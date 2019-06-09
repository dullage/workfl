import re

BLANK_LINE_RE = re.compile(r"\s*$")


class ws:
    @classmethod
    def _escape(cls, string):
        string = string.replace("\#", "&hash!")
        string = string.replace("\|", "&pipe!")

        return string

    @classmethod
    def _unescape(cls, string):
        string = string.replace("&hash!", "#")
        string = string.replace("&pipe!", "|")

        return string

    @classmethod
    def _strip_comments(cls, markup):
        stripped_markup = ""
        # comment_char_re = re.compile(r"[^\\](#)")

        for input_line in markup.splitlines():
            # Keep blank lines as they end flows.
            if re.match(BLANK_LINE_RE, input_line):
                output_line = input_line

            else:
                comment_char_i = input_line.find("#")

                # Remove lines that are entirely commented. This allows comment
                # lines to be inserted within a flow but without breaking it.
                if comment_char_i == 0:
                    output_line = None

                # Strip any inline comments and add the rest of the line.
                elif comment_char_i > 0:
                    output_line = input_line[0:comment_char_i]

                # No comment characters, just add the line back.
                else:
                    output_line = input_line

            if output_line is not None:
                # Add the line.
                stripped_markup += output_line + "\n"

        return stripped_markup

    def _parse_node_line(self, line):
        contents = line.split("|", maxsplit=2)
        contents_len = len(contents)

        # TODO: strip() only once
        if contents_len >= 3:
            id = self._unescape(contents[2].lower().strip())
            label = self._unescape(contents[0].strip())
        else:
            id = self._unescape(contents[0].lower().strip())
            label = self._unescape(contents[0].strip())

        if contents_len >= 2:
            description = self._unescape(contents[1].strip())
        else:
            description = None

        return id, label, description

    def _add_node(self, id, label, description=None):
        if id in self._nodes.keys():
            return id
        else:
            self._nodes[id] = {
                "label": label,
                "description": description,
                "connection_ids": [],
            }

        return id

    def _parse_connection_description_line(self, line):
        contents = line.split("|", maxsplit=1)
        contents_len = len(contents)

        label = self._unescape(contents[0].strip())

        if contents_len >= 2:
            description = self._unescape(contents[1].strip())
        else:
            description = None

        return label, description

    def _add_connection(
        self, from_node_id, to_node_id, label=None, description=None
    ):
        connection_id = self._max_connection_id + 1

        self._connections[connection_id] = {
            "from_node_id": from_node_id,
            "to_node_id": to_node_id,
            "label": label,
            "description": description,
        }

        self._nodes[from_node_id]["connection_ids"].append(connection_id)
        self._nodes[to_node_id]["connection_ids"].append(connection_id)

        self._max_connection_id = connection_id

        return connection_id

    def _parse_stripped_markup(self):
        prev_node_id = None
        connection_label = None
        connection_desc = None

        for line in self._markup_clean.splitlines():
            # Blank lines indicate the end of a flow.
            if re.match(BLANK_LINE_RE, line):
                prev_node_id = None
                connection_label = None
                connection_desc = None

            # Lines that begin with whitespace indicate a connection
            # description.
            elif line[0] in (" ", "\t"):
                connection_label, connection_desc = self._parse_connection_description_line(
                    line
                )

            # Other lines are nodes within a flow.
            else:
                node_id, label, description = self._parse_node_line(line)
                self._add_node(node_id, label, description=description)
                if prev_node_id:
                    self._add_connection(
                        prev_node_id,
                        node_id,
                        label=connection_label,
                        description=connection_desc,
                    )
                prev_node_id = node_id
                connection_label = None
                connection_desc = None

    @classmethod
    def _clean_markup(cls, markup):
        markup = cls._escape(markup)
        markup = cls._strip_comments(markup)

        return markup

    def __init__(self, markup):
        self._markup_raw = markup
        self._markup_clean = self._clean_markup(markup)

        self._nodes = {}
        self._max_connection_id = -1
        self._connections = {}

        self._parse_stripped_markup()

    def __str__(self):
        return self._markup_raw

    @property
    def markup(self):
        return self._markup_raw

    @property
    def markup_stripped(self):
        return self._markup_clean

    @property
    def nodes(self):
        return self._nodes

    @property
    def connections(self):
        return self._connections

    @classmethod
    def _build_mermaid_line(
        cls,
        node_id,
        node_label,
        to_node_id=None,
        to_node_label=None,
        connection_label=None,
    ):
        from_node = '{}("{}")'.format(node_id, node_label)

        connection = to_node = ""
        if to_node_id and to_node_label:
            connection = "-->"
            to_node = '{}("{}")'.format(to_node_id, to_node_label)

        if connection and connection_label:
            connection += '|"{}"|'.format(connection_label)

        line = "  {}{}{};".format(from_node, connection, to_node)

        return line

    def _generate_mermaid_ids(self):
        new_id = 0
        for id, node in self._nodes.items():
            node["mermaid_id"] = new_id
            new_id += 1

    def to_mermaid(self, direction="TB"):
        self._generate_mermaid_ids()

        direction = direction.upper()
        if direction not in ["TB", "BT", "LR", "RL"]:
            direction = "TB"

        mermaid = "graph {}\n".format(direction)

        # Add unconnected nodes
        for id, node in self._nodes.items():
            if not node["connection_ids"]:
                mermaid += self._build_mermaid_line(id, node["label"])

        # Add connected nodes
        for connection_id, connection in self._connections.items():
            from_node = self._nodes[connection["from_node_id"]]
            to_node = self._nodes[connection["to_node_id"]]

            mermaid += (
                self._build_mermaid_line(
                    from_node["mermaid_id"],
                    from_node["label"],
                    to_node["mermaid_id"],
                    to_node["label"],
                    connection["label"],
                )
                + "\n"
            )

        return mermaid
