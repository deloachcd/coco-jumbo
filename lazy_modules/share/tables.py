import attr


@attr.s
class DisplayTable:
    """Class for displaying tabular output in the console, heavily based on
    org-mode tables."""

    layout = attr.ib()
    collection = attr.ib()
    stringify = attr.ib(default=str)

    def __str__(self):
        return "DisplayTable({})".format(", ".join(list(self.layout.keys())))

    def render(self, borderless=False):
        column_headers = list(self.layout.keys())
        column_content = [
            [self.stringify(function(item)) for item in self.collection]
            for function in self.layout.values()
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
        Jojo("giorno", "has a dream", "gold experience")
    ]

    jojo_table = DisplayTable(
        {
            "Name": lambda jojo: jojo.get_name(),
            "Description": lambda jojo: jojo.get_description(),
            "Stand": lambda jojo: jojo.get_stand(),
        },
        jojos,
    )

    print(jojo_table.render())
    print()
    print(jojo_table.render(borderless=True))
