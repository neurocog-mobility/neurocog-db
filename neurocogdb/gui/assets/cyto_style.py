STYLESHEET = [
    {
        "selector": "node",
        "style": {
            "label": "data(label)",
            "text-valign": "center",
            "text-halign": "center",
            "text-wrap": "wrap",
            "white-space": "pre-line",
        },
    },
    {
        "selector": "node.highlighted",
        "style": {
            "border-color": "#FFD700",
            "border-width": 4,
            "background-color": "#FFD700",
            "color": "black",
        },
    },
    {
        "selector": "edge.highlighted",
        "style": {
            "line-color": "#FFD700",
            "width": 3,
        },
    },
    {
        "selector": '[type="program"]',
        "style": {
            "background-color": "#292929",
            "shape": "round-rectangle",
            "color": "white",
            "font-size": "6rem",
            "font-weight": "bold",
        },
    },
    {
        "selector": '[type="project"]',
        "style": {
            "background-color": "#2E5A88",
            "shape": "round-rectangle",
            "color": "white",
            "font-weight": "600",
            "font-size": "6rem",
            "border-width": "2px",
        },
    },
    {
        "selector": '[type="project"][status="ongoing"]',
        "style": {"border-color": "#ff7f0e"},  # blue
    },
    {
        "selector": '[type="project"][status="completed"]',
        "style": {"border-color": "#55d655"},  # green
    },
    {
        "selector": '[type="project"][status="upcoming"]',
        "style": {"border-color": "white"},
    },
    {
        "selector": '[type="member"]',
        "style": {
            "background-color": "white",
            "shape": "round-rectangle",
            "color": "black",
            "font-size": "6rem",
            "border-width": "1px",
            "border-color": "#CCCCCC",
        },
    },
    {
        "selector": '[type="collaborator"]',
        "style": {
            "background-color": "#C5DEF2",
            "shape": "round-rectangle",
            "color": "black",
            "font-size": "6rem",
        },
    },
    {
        "selector": '[type="funding"]',
        "style": {
            "background-color": "#ffb6b6",
            "shape": "round-rectangle",
            "color": "black",
            "font-size": "6rem",
        },
    },
    {
        "selector": "edge",
        "style": {
            "curve-style": "bezier",
            "target-arrow-shape": "vee",
            "label": "data(label)",
            "font-size": "4rem",
        },
    },
]
