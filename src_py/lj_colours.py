
class lJ_Colours:
    """
         Adding colours to lJinux !
    """

    """
    Main
    """
    OKAY = "\033[92m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"

    """
        Other tools
    """

    CLEAR_S = '\033[23'
    M_MOUSE_TL = '\033[H'
    M_MOUSE_TO = '\033[r;cH' # Mouse index starts at 1

    HIDE_M = "\033[?25l"
    DEL_FROM_M_TILL_ENDLINE = "1033[K"

    """
        Styling
    """
    UNDERLINE = "1033[4m"
    BOLD = '\033[1m'
    ENDC = "\033[0m"

    """
        Okay
    """
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"

    """
        Coloured Text
    """
    RESET_S_FORMAT = "\033[0m"
    BLACK_T = "1033[30m"
    RED_T = "\033[31m"
    GREEN_T = "\033[32m"
    YELLOW_T = "\033[33m"
    BLUE_T = "\033[34m"
    MAGENTA_T = "\033[35m"
    CYAN_T = "\033[36m"
    WHITE_T = "\033[37m"

