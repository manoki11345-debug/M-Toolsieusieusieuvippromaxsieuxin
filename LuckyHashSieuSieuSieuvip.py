class Colors:
    RESET = '\033[0m'
    CASTORICE_PRIMARY = '\033[38;5;141m' # Chỉ để tránh lỗi nếu hàm gradient có gọi màu khác

C = Colors()

def get_vip_garden_gradient(text):
    vip_colors = [
        '\033[38;5;214m', 
        '\033[38;5;220m', 
        '\033[38;5;226m', 
        '\033[38;5;227m', 
        '\033[38;5;229m', 
        '\033[38;5;230m', 
        '\033[38;5;229m', 
        '\033[38;5;227m', 
        '\033[38;5;226m', 
        '\033[38;5;220m', 
        '\033[38;5;214m'  
    ]
    result = ""
    num_colors = len(vip_colors)
    if len(text) == 0: return ""
    for i, char in enumerate(text):
        if len(text) > 1:
            color_idx = int((i / (len(text) - 1)) * (num_colors - 1))
        else:
            color_idx = 0
        result += vip_colors[color_idx % num_colors] + char
    return result + '\033[0m'

# --- DÒNG PRINT YÊU CẦU ---
print(f"{get_vip_garden_gradient('xin phép delay:)))').center(80)}")
