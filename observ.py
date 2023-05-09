def printloc():
    # M1
    x, y = 53.94, 60.94
    w, h = 19.04, 22.42

    tl = (x - w/2, y - h/2)
    tr = (x + w/2, y - h/2)
    bl = (x - w/2, y + h/2)
    br = (x + w/2, y + h/2)

    print("M1:")
    print(f"Top-left corner: {tl}")
    print(f"Top-right corner: {tr}")
    print(f"Bottom-left corner: {bl}")
    print(f"Bottom-right corner: {br}")
    print()

    # M2
    x, y = 69.49, 70.85
    w, h = 11.92, 19.74

    tl = (x - w/2, y - h/2)
    tr = (x + w/2, y - h/2)
    bl = (x - w/2, y + h/2)
    br = (x + w/2, y + h/2)

    print("M2:")
    print(f"Top-left corner: {tl}")
    print(f"Top-right corner: {tr}")
    print(f"Bottom-left corner: {bl}")
    print(f"Bottom-right corner: {br}")
    print()

    # R
    x, y = 112.67, 14.86
    r = 13.3

    tl = (x - r, y - r)
    tr = (x + r, y - r)
    bl = (x - r, y + r)
    br = (x + r, y + r)

    print("R:")
    print(f"Top-left corner: {tl}")
    print(f"Top-right corner: {tr}")
    print(f"Bottom-left corner: {bl}")
    print(f"Bottom-right corner: {br}")
    print()

    # B
    x, y = 16.60, 110.02
    r = 13.3

    tl = (x - r, y - r)
    tr = (x + r, y - r)
    bl = (x - r, y + r)
    br = (x + r, y + r)

    print("B:")
    print(f"Top-left corner: {tl}")
    print(f"Top-right corner: {tr}")
    print(f"Bottom-left corner: {bl}")
    print(f"Bottom-right corner: {br}")
