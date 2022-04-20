class lJ_Colours:
    """
    Adding colours to lJinux !
    """

    """
    Main
    """
    okay = "\033[92m"
    warning = "\033[93m"
    error = "\033[91m"

    """
        Other tools
    """

    clear_s = "\033[23"
    m_mouse_tl = "\033[H"
    m_mouse_to = "\033[r;cH"  # Mouse index starts at 1

    hide_m = "\033[?25l"
    del_from_m_till_endline = "1033[K"

    """
        Styling
    """
    underline = "\033[4m"
    bold = "\033[1m"
    endc = "\033[0m"  # use to end color

    """
        Okay
    """
    okblue = "\033[94m"
    okcyan = "\033[96m"

    """
        Coloured Text
    """
    reset_s_format = "\033[0m"
    black_t = "\033[30m"
    red_t = "\033[31m"
    green_t = "\033[32m"
    yellow_t = "\033[33m"
    blue_t = "\033[34m"
    magenta_t = "\033[35m"
    cyan_t = "\033[36m"
    white_t = "\033[37m"
