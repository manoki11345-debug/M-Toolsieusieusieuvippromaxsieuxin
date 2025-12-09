class Colors:
    RESET = '\033[0m'
    CASTORICE_PRIMARY = '\033[38;5;141m' # Chỉ cần để tránh lỗi nếu hàm gradient có gọi màu khác

C = Colors()

GREEN_GARDEN = ['\033[38;5;23m', '\033[38;5;24m', '\033[38;5;30m', '\033[38;5;42m', '\033[38;5;120m', '\033[38;5;157m', '\033[38;5;194m', '\033[38;5;157m', '\033[38;5;120m', '\033[38;5;42m', '\033[38;5;30m', '\033[38;5;24m', '\033[38;5;23m']

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

# --- Vua Thoát Hiểm --- Màu free cho ae luôn nha
print(f"{custom_gradient('Tool đang update, vui lòng đợi', GREEN_GARDEN).center(80)}")
