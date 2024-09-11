import dash_mantine_components as dmc
from utils.website_text import TextFooter


def my_footer():
    return dmc.Group(
        children=[
            dmc.Grid(
                children=[
                    dmc.GridCol(
                        dmc.Group(
                            [
                                dmc.Image(
                                    src="/assets/media/CBE-logo-2019-white.png",
                                    maw=150,
                                    p="1rem",
                                    alt="logo CBE",
                                ),
                                dmc.Image(
                                    src="/assets/media/ucb-logo-2024-white.png",
                                    maw=180,
                                    p="1rem",
                                    alt="berkeley_logo",
                                ),
                            ],
                            align="center",
                            justify="center",
                            gap="xs",
                        ),
                        span={"base": 12, "md": 4},
                    ),
                    dmc.GridCol(
                        dmc.Center(
                            dmc.Anchor(
                                dmc.Text(
                                    TextFooter.contact_us.value,
                                    c="white",
                                ),
                                href=TextFooter.contact_us_link.value,
                            ),
                        ),
                        span={"base": 12, "md": 1},
                    ),
                    dmc.GridCol(
                        dmc.Center(
                            dmc.Anchor(
                                dmc.Text(
                                    TextFooter.report_issues.value,
                                    c="white",
                                ),
                                href=TextFooter.report_issues_link.value,
                            ),
                        ),
                        span={"base": 12, "md": 1},
                    ),
                    dmc.GridCol(
                        dmc.Group(
                            [
                                dmc.Anchor(
                                    dmc.Image(
                                        src="/assets/media/github-white-transparent.png",
                                        maw=45,
                                        alt="github logo",
                                    ),
                                    href="#",
                                ),
                                dmc.Anchor(
                                    dmc.Image(
                                        src="/assets/media/linkedin-white.png",
                                        maw=45,
                                        alt="linkedin logo",
                                    ),
                                    href="#",
                                ),
                            ],
                            align="center",
                            justify="center",
                            gap="xl",
                        ),
                        span={"base": 12, "md": 2},
                    ),
                    dmc.GridCol(
                        dmc.Stack(
                            [
                                dmc.Text(
                                    TextFooter.cite_strong.value,
                                    fw=700,
                                    c="white",
                                    size="sm",
                                ),
                                dmc.Group(
                                    [
                                        dmc.Text(
                                            TextFooter.cite.value,
                                            c="white",
                                            size="sm",
                                        ),
                                        dmc.Anchor(
                                            dmc.Text(
                                                TextFooter.cite_link.value,
                                                c="white",
                                                size="sm",
                                                td="underline",
                                            ),
                                            href=TextFooter.cite_link.value,
                                        ),
                                    ],
                                    gap=0,
                                ),
                            ],
                            align="center",
                            justify="center",
                            mt=5,
                            mb=5,
                            mr=20,
                            ml=40,
                            gap=0,
                        ),
                        span={"base": 12, "md": 4},
                    ),
                ],
                align="center",
                justify="center",
                bg="#0077c2",
                w="100%",
            ),
            dmc.Grid(
                children=[
                    dmc.GridCol(
                        dmc.Text(
                            TextFooter.copy_right.value,
                            c="white",
                            size="xs",
                        ),
                        span={"base": 12, "md": 10},
                    ),
                    dmc.GridCol(
                        dmc.Text(
                            TextFooter.version.value,
                            c="white",
                            size="xs",
                        ),
                        span={"base": 6, "md": 1},
                    ),
                    dmc.GridCol(
                        dmc.Anchor(
                            dmc.Image(
                                src="/assets/License-MIT-yellow.svg",
                                w="6rem",
                                alt="license mit logo",
                            ),
                            href=TextFooter.open_source_link.value,
                        ),
                        span={"base": 6, "md": 1},
                    ),
                ],
                align="center",
                bg="#0c2772",
                w="100%",
                p="1rem",
            ),
        ],
        gap=0,
        w="100%",
    )
