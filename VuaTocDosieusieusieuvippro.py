class Colors:
    RESET = '\033[0m'
    CASTORICE_PRIMARY = '\033[38;5;141m' # Chỉ cần để tránh lỗi nếu hàm gradient có gọi màu khác

C = Colors()

LAVA_GARDEN = ['\033[38;5;124m', '\033[38;5;166m', '\033[38;5;202m', '\033[38;5;208m', '\033[38;5;214m', '\033[38;5;226m', '\033[38;5;214m', '\033[38;5;208m', '\033[38;5;202m', '\033[38;5;166m', '\033[38;5;124m']

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

# --- Vua Tốc Độ --- Màu free lấy thoải mái nha
print(f"{custom_gradient('Tool đang trong quá trình phát triển', LAVA_GARDEN).center(80)}")
          
