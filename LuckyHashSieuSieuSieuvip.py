import sys

class Colors:
    RESET = '\033[0m'
    CASTORICE_PRIMARY = '\033[38;5;141m'

C = Colors()

YELLOW_GARDEN = ['\033[38;5;214m', '\033[38;5;220m', '\033[38;5;226m', '\033[38;5;227m', '\033[38;5;229m', '\033[38;5;230m', '\033[38;5;229m', '\033[38;5;227m', '\033[38;5;226m', '\033[38;5;220m', '\033[38;5;214m']

def custom_gradient(text, colors):
    result = ""
    num_colors = len(colors)
    if len(text) <= 1:
        return colors[0] + text + C.RESET
    for i, char in enumerate(text):
        if len(text) > 1:
            color_idx = int((i / (len(text) - 1)) * (num_colors - 1))
        else:
            color_idx = 0
        result += colors[color_idx] + char
    return result + C.RESET

print(f"{custom_gradient('Bên Trịnh Đang Lỗi Obfuscate ae qua TnTool nha', YELLOW_GARDEN).center(80)}")

sys.exit(0)
