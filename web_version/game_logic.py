# game_logic.py

QUESTION_DATA = [
    {
        "prompt": "Q1: Your group is behind on a big assignment. One person hasn’t done their part, and the deadline’s tomorrow.",
        "filename": "data/bapst_pixelated.png",
        "options": [
            "Redo the missing section yourself so the project looks polished",
            "Call a group meeting to talk it through",
            "Redesign the slides to make them more engaging",
            "Email the professor asking for an extension and explain the issue",
            "Offer to lead a late-night work session with snacks",
            "Help everyone manage stress and remind them it’s just one grade",
            "Check in with the missing person privately",
        ],
        "scores": [
            (2, 0, 0, 1, 1, 0, 0),
            (1, 2, 0, 0, 0, 0, 1),
            (1, 1, 2, 0, 0, 0, 0),
            (1, 0, 0, 2, 0, 0, 1),
            (1, 1, 0, 0, 2, 0, 0),
            (0, 1, 0, 0, 0, 2, 1),
            (0, 1, 0, 0, 0, 1, 2),
        ]
    },
    {
        "prompt": "Q2: You’re wandering through the annual student club fair. What table grabs your attention?",
        "filename": "data/quad_pixelated.png",
        "options": [
            "One with flyers about scholarships and research opportunities.",
            "A table playing loud music and handing out stickers.",
            "A booth with students painting a banner",
            "A group giving out buttons about voting rights.",
            "A sports demo where you can try rock climbing",
            "A table sharing foods from different cultures.",
            "A quiet setup with candles for meditation and reflection.",
        ],
        "scores": [
            (2, 0, 1, 1, 0, 0, 0),
            (0, 2, 1, 0, 1, 0, 0),
            (0, 0, 2, 1, 0, 0, 1),
            (1, 0, 0, 2, 0, 0, 1),
            (1, 1, 0, 0, 2, 0, 0),
            (0, 1, 0, 0, 0, 1, 2),
            (0, 0, 1, 0, 0, 2, 1),
        ]
    },
    {
        "prompt": "Q3: It’s 11:30 PM and you’ve just finished studying. You have an early class tomorrow, but your phone buzzes with an invite.",
        "filename": "data/ignatius_pixelated.png",
        "options": [
            "Stay up and finish revising your notes — you’ll thank yourself later.",
            "Go to your friend’s room to hang out and decompress.",
            "Start sketching because you’re suddenly inspired.",
            "Join a late-night discussion about campus policies.",
            "Lace up your shoes for a quick run under the stars.",
            "Call your mom and talk about something you’ve been thinking about.",
            "Sit quietly for ten minutes to reflect before bed.",
        ],
        "scores": [
            (2, 0, 0, 0, 1, 1, 0),
            (0, 2, 1, 0, 0, 0, 1),
            (0, 1, 2, 0, 0, 1, 0),
            (1, 1, 0, 2, 0, 0, 0),
            (1, 0, 0, 0, 2, 1, 0),
            (0, 1, 0, 0, 0, 1, 2),
            (0, 0, 1, 0, 0, 2, 1),
        ]
    },
    {
        "prompt": "Q4: Your professor mentions a community service opportunity this weekend. What catches your interest?",
        "filename": "data/red_tree_pixelated.png",
        "options": [
            "Tutoring local kids",
            "Organizing a charity 5K",
            "Creating posters to advertise the event.",
            "Volunteering at a cultural center.",
            "Helping manage logistics and schedules.",
            "Preparing a reflection or prayer for the closing.",
            "Helping spread the word among other communities",
        ],
        "scores": [
            (2, 0, 0, 1, 0, 0, 1),
            (1, 0, 0, 1, 2, 0, 0),
            (1, 0, 2, 1, 0, 0, 0),
            (0, 1, 0, 0, 0, 1, 2),
            (1, 2, 0, 0, 1, 0, 0),
            (0, 0, 1, 0, 0, 2, 1),
            (1, 1, 0, 2, 0, 0, 0),
        ]
    },
    {
        "prompt": "Q5: It’s a rare free morning. How do you spend it?",
        "filename": "data/gasson_pixelated.png",
        "options": [
            "Plan your week and set new goals.",
            "Brunch with friends — you need to catch up.",
            "Work on your photography project outside.",
            "Attend a social justice workshop on campus.",
            "Join an intramural scrimmage.",
            "Cook a traditional meal with your roommates.",
            "Walk to a quiet garden to clear your mind.",
        ],
        "scores": [
            (2, 0, 0, 0, 1, 1, 0),
            (0, 2, 1, 0, 0, 0, 1),
            (1, 0, 2, 0, 0, 1, 0),
            (0, 0, 0, 2, 0, 1, 1),
            (1, 1, 0, 0, 2, 0, 0),
            (0, 1, 0, 0, 0, 1, 2),
            (0, 0, 1, 0, 0, 2, 1),
        ]
    }
]

CLUBS = {
    "Achiever": [
        {
            "name":"Boston College Computer Science Society",
            "image": "bc_pixelated.png",
        },
        {
            "name":"Investment Club",
            "image": "bc_pixelated.png",
        },
    ],
    "Social": [
        {
            "name":"Campus Activities Board",
            "image": "bc_pixelated.png",
        },
        {
            "name":"Cooking Club",
            "image": "bc_pixelated.png",
        },
    ],
    "Creative":  [
        {
            "name":"Art Club",
            "image": "bc_pixelated.png",
        },
        {
            "name":"Symphony Orchestra",
            "image": "bc_pixelated.png",
        },
    ],
    "Activist":  [
        {
            "name":"EcoPledge",
            "image": "bc_pixelated.png",
        },
        {
            "name":"Ignatian Family Teach-in",
            "image": "bc_pixelated.png",
        },
    ],
    "Athlete":  [
        {
            "name":"Basketball Club",
            "image": "bc_pixelated.png",
        },
        {
            "name":"Ultimate Frisbee",
            "image": "bc_pixelated.png",
        },
    ],
    "Spiritual":  [
        {
            "name":"BC ALIVE",
            "image": "bc_pixelated.png",
        },
        {
            "name":"InterVarsity",
            "image": "bc_pixelated.png",
        },
    ],
    "Cultural":  [
        {
            "name":"International Club",
            "image": "bc_pixelated.png",
        },
        {
            "name":"Chinese Students Association",
            "image": "bc_pixelated.png",
        },
    ],
}

def calculate_results(scores):
    categories = [
        "Achiever", "Social", "Creative",
        "Activist", "Athlete", "Spiritual", "Cultural"
    ]

    ranked = sorted(
        zip(categories, scores),
        key=lambda x: x[1],
        reverse=True
    )

    seen = set()
    results = []
    for cat, score in ranked:
        if cat not in seen:
            results.append({
                "category": cat,
                "clubs": CLUBS[cat]
                })
            seen.add(cat)

        if len(results) == 2:
            break

    return results
