class DisplayTable:
    """Class for displaying tabular output in the console, heavily based on
    org-mode tables."""

    # layout = attr.ib()
    # collection = attr.ib()
    # stringify = attr.ib(default=str)

    def __init__(self, layout, collection, stringify=str):
        self.layout = layout
        self.collection = collection
        self.stringify = stringify

    def __str__(self):
        return "DisplayTable({})".format(", ".join(list(self.layout.keys())))

    def __repr__(self):
        return "{}(layout={},collection={},stringify={})".format(
            self.__class__, self.layout, self.collection, self.stringify
        )

    @classmethod
    def from_2d_array(cls, array2d):
        layout = {}
        headers = array2d[0]
        for i, header in enumerate(headers):
            # 'eval' used to hack around python's default behavior of
            # evaluating expressions within function definition when called
            layout[header] = eval("lambda entry: entry[{}]".format(i))
        return cls(layout, array2d[1:])

    def render(self, borderless=False, index_column=False):
        if index_column:
            column_headers = ["#"] + list(self.layout.keys())
            column_content = [[str(i + 1) for i in range(len(self.collection))]] + [
                [self.stringify(function(item)) for item in self.collection]
                for i, function in enumerate(self.layout.values())
            ]
            pass
        else:
            column_headers = list(self.layout.keys())
            column_content = [
                [self.stringify(function(item)) or item[i] for item in self.collection]
                for i, function in enumerate(self.layout.values())
            ]
        column_widths = [max(map(len, column)) for column in column_content]
        for i, width in enumerate(column_widths):
            if len(column_headers[i]) > width:
                column_widths[i] = len(column_headers[i])

        if borderless:
            sep = " "
        else:
            sep = "|"
        header_row = sep.join(
            [
                " {}{} ".format(
                    column_headers[i], (width - len(column_headers[i])) * " "
                )
                for i, width in enumerate(column_widths)
            ]
        )

        if borderless:
            row_join = "\n"
        else:
            row_join = "|\n|"
            seperator_row = "+".join(["-" * (width + 2) for width in column_widths])
        content_rows = row_join.join(
            [
                sep.join(
                    [
                        " {}{} ".format(
                            column_content[i][j],
                            (column_widths[i] - len(column_content[i][j])) * " ",
                        )
                        for i in range(len(column_content))
                    ]
                )
                for j in range(len(column_content[0]))
            ]
        )

        if borderless:
            return "{}\n{}".format(header_row, content_rows)
        else:
            return "|{}|\n|{}|\n|{}|".format(header_row, seperator_row, content_rows)


if __name__ == "__main__":
    """This is used to test our table-rendering implementation"""

    class Jojo:
        def __init__(self, name, description, stand):
            self.name = name
            self.description = description
            self.stand = stand

        def get_name(self):
            return self.name

        def get_description(self):
            return self.description

        def get_stand(self):
            return self.stand

    jojos = [
        Jojo("jonathan", "hamon specialist and gentleman", None),
        Jojo("joseph", "master of asspulls", "hermit purple"),
        Jojo("jotaro", "had a steamroller dropped on him; survived", "star platinum"),
        Jojo("josuke", "willing to punch a hole through his own mom", "crazy diamond"),
        Jojo("giorno", "has a dream", "gold experience"),
    ]

    jojos_array2d = [
        ["Name", "Description", "Stand"],
        ["jonathan", "hamon specialist and gentleman", None],
        ["joseph", "master of asspulls", "hermit purple"],
        ["jotaro", "had a steamroller dropped on him; survived", "star platinum"],
        ["josuke", "willing to punch a hole through his own mom", "crazy diamond"],
        ["giorno", "has a dream", "gold experience"],
    ]

    jojo_table = DisplayTable(
        {
            "Name": lambda jojo: jojo.get_name(),
            "Description": lambda jojo: jojo.get_description(),
            "Stand": lambda jojo: jojo.get_stand(),
        },
        jojos,
    )

    jojo_a2d_table = DisplayTable.from_2d_array(jojos_array2d)

    print(jojo_table.render())
    print()
    print(jojo_table.render(borderless=True))
    print()
    print(jojo_a2d_table.render(index_column=True))
    print()
    print(jojo_a2d_table.render(borderless=True, index_column=True))
