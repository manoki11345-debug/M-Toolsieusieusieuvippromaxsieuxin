import requests
import json
import time
import os
import sys
import re
import math
import random
import base64
from collections import deque, Counter
from datetime import datetime, timedelta
import threading
import pytz

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    os.system("pip install requests colorama pytz")
    sys.exit()

class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    PRIMARY = '\033[38;5;141m'
    SECONDARY = '\033[38;5;117m'
    SUCCESS = '\033[38;5;120m'
    WARNING = '\033[38;5;221m'
    ERROR = '\033[38;5;210m'
    INFO = '\033[38;5;159m'
    ACCENT = '\033[38;5;183m'
    MUTED = '\033[38;5;250m'
    WHITE = '\033[97m'
    
    GOLD_1 = '\033[38;5;220m'
    
    GRAD1 = '\033[38;5;147m'
    GRAD2 = '\033[38;5;153m'
    GRAD3 = '\033[38;5;159m'
    
    ORANGE = '\033[38;5;208m'
    YELLOW = '\033[38;5;220m'

    TT8_GREEN_PRIMARY = '\033[38;5;114m'
    
    CASTORICE_PRIMARY = '\033[38;5;141m'
    CASTORICE_SECONDARY = '\033[38;5;177m'
    CASTORICE_ACCENT = '\033[38;5;183m'
    CASTORICE_LIGHT = '\033[38;5;189m'

C = Colors()

API_URL_CREATE_ORDER = "https://api.winhash.net/lucky_hash/create_order"
API_URL_GET_BALANCE = "https://wallet.3games.io/api/wallet/user_asset"
__SECURE_ENDPOINT = "https://manokey.neocities.org/Castorice_key=PhungTanSangYeuCastoriceratnhieu-ManoKey/Keyvipsieusieuvip/yeucastorice/"
LOCAL_DONATE_KEY_FILE = "mano_donate_key.json"
FREE_KEY_FILE = "mano_free_key.json"

Mano_ODDS = 1.6999
Mano_NUM_LEFT = 54.12
Mano_NUM_RIGHT = 45.87
THEORETICAL_SMALL_PROB = 0.5412

ACTIVE_KEY_TYPE: str = "FREE"
tz = pytz.timezone("Asia/Ho_Chi_Minh")

def clear(): 
    os.system('cls' if os.name=='nt' else 'clear')

def exit_tool_with_error():
    print(f"\n{C.ERROR}Lỗi. Liên hệ admin để được hỗ trợ{C.RESET}")
    time.sleep(3)
    sys.exit(1)

def encrypt_data(data):
    try:
        return base64.b64encode(data.encode()).decode()
    except:
        exit_tool_with_error()

def decrypt_data(encrypted_data):
    try:
        return base64.b64decode(encrypted_data.encode()).decode()
    except:
        exit_tool_with_error()

def get_ip_address():
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        ip_data = response.json()
        return ip_data.get('ip')
    except Exception:
        return None

def get_castorice_gradient(text):
    castorice_colors_smooth = [
        '\033[38;5;93m', '\033[38;5;99m', '\033[38;5;135m', '\033[38;5;141m',
        '\033[38;5;177m', '\033[38;5;183m', '\033[38;5;189m', '\033[38;5;219m',
        '\033[38;5;189m', '\033[38;5;183m', '\033[38;5;177m', '\033[38;5;141m',
        '\033[38;5;135m', '\033[38;5;99m', '\033[38;5;93m'
    ]
    num_colors = len(castorice_colors_smooth)
    result = ""
    for i, char in enumerate(text):
        if len(text) > 1:
            color_idx = int((i / (len(text) - 1)) * (num_colors - 1))
        else:
            color_idx = 0
        result += castorice_colors_smooth[color_idx % num_colors] + char
    return result + '\033[0m'

def get_vip_garden_gradient(text):
    vip_colors = [
        '\033[38;5;214m', '\033[38;5;220m', '\033[38;5;226m', 
        '\033[38;5;227m', '\033[38;5;229m', '\033[38;5;230m', 
        '\033[38;5;229m', '\033[38;5;227m', '\033[38;5;226m',
        '\033[38;5;220m', '\033[38;5;214m' 
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

def fetch_server_keys_secure():
    try:
        target = f"{__SECURE_ENDPOINT}?t={int(time.time())}"
        response = requests.get(target, timeout=15)
        if response.status_code == 200:
            response.encoding = 'utf-8' 
            content = response.text.strip()
            if content.startswith(u'\ufeff'):
                content = content[1:]
            return json.loads(content)
    except:
        pass
    return None

def verify_key_strict(key_input, current_ip_check):
    server_data = fetch_server_keys_secure()
    if not server_data:
        return False, "SERVER_ERROR", None
    if key_input not in server_data:
        return False, "KEY_NOT_FOUND", None
    key_info = server_data[key_input]
    registered_ip_str = str(key_info.get("ip", "all")).strip()
    expiry_str = key_info.get("expiry", "")
    description = key_info.get("desc", "Thành viên VIP")
    allowed_ips = [x.strip() for x in registered_ip_str.split(',')]
    if "all" not in allowed_ips:
        if current_ip_check not in allowed_ips:
            return False, "IP_LOCKED", None
    try:
        vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S")
        expiry_date = vn_tz.localize(expiry_date)
        now_vn = datetime.now(vn_tz)
        if now_vn > expiry_date:
            return False, "KEY_EXPIRED", None
        diff = expiry_date - now_vn
        days = diff.days
        seconds = diff.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        time_left_msg = f"{days} ngày, {hours} giờ, {minutes} phút"
        return True, time_left_msg, description
    except ValueError:
        return False, "DATE_FORMAT_ERROR", None
    except Exception:
        return False, "UNKNOWN_AUTH_ERROR", None

def save_local_donate_key(key):
    try:
        data = {'key': key}
        encrypted_data = encrypt_data(json.dumps(data))
        with open(LOCAL_DONATE_KEY_FILE, 'w', encoding='utf-8') as f:
            f.write(encrypted_data)
        return True
    except:
        exit_tool_with_error()

def load_local_donate_key():
    try:
        if os.path.exists(LOCAL_DONATE_KEY_FILE):
            with open(LOCAL_DONATE_KEY_FILE, 'r', encoding='utf-8') as f:
                encrypted_data = f.read()
                decrypted = decrypt_data(encrypted_data)
                return json.loads(decrypted)
        return None
    except:
        return None

def check_local_donate_key(ip_address: str):
    local_data = load_local_donate_key()
    if not local_data:
        return False, "NO_KEY", None 
    saved_key = local_data.get('key')
    if not saved_key:
        try:
            os.remove(LOCAL_DONATE_KEY_FILE)
        except:
            pass
        return False, "KEY_CORRUPTED", None

    is_valid, msg, desc = verify_key_strict(saved_key, ip_address)
    if is_valid:
        full_msg = msg
        if desc:
            full_msg = f"{msg} | {desc}"
        return True, full_msg, saved_key
    else:
        try:
            os.remove(LOCAL_DONATE_KEY_FILE)
        except:
            pass
        return False, msg, None

def generate_key_and_url(ip_address):
    try:
        now = datetime.now(tz)
        ngay = int(now.day)
        key1 = str(ngay * 27 + 27)
        ip_numbers = ''.join(filter(str.isdigit, ip_address))
        key = f'MANO-{key1}{ip_numbers}'
        expiration_date = now.replace(hour=23, minute=59, second=0, microsecond=0)
        return key, expiration_date
    except:
        exit_tool_with_error()

def save_local_free_key(key, expiration_date):
    try:
        data = {'key': key, 'expiration_date': expiration_date.isoformat()}
        encrypted_data = encrypt_data(json.dumps(data))
        with open(FREE_KEY_FILE, 'w', encoding='utf-8') as file:
            file.write(encrypted_data)
        return True
    except:
        exit_tool_with_error()

def load_local_free_key():
    try:
        if os.path.exists(FREE_KEY_FILE):
            with open(FREE_KEY_FILE, 'r', encoding='utf-8') as file:
                encrypted_data = file.read()
            data = json.loads(decrypt_data(encrypted_data))
            return data
        return None
    except:
        return None

def kiem_tra_ip_free(ip_address: str):
    local_data = load_local_free_key()
    
    expected_key, expected_expiry_date = generate_key_and_url(ip_address)
    
    if not local_data:
        return False, "NO_FREE_KEY", None

    saved_key = local_data.get('key')
    expiry_str = local_data.get('expiration_date')

    if not saved_key or not expiry_str:
        try:
            os.remove(FREE_KEY_FILE)
        except:
            pass
        return False, "KEY_CORRUPTED", None
    
    if saved_key != expected_key:
        try:
            os.remove(FREE_KEY_FILE)
        except:
            pass
        return False, "KEY_CHANGED", None

    try:
        vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        expiration_date = datetime.fromisoformat(expiry_str)
        expiration_date = vn_tz.localize(expiration_date.replace(tzinfo=None))
        now_vn = datetime.now(vn_tz)
    
        if now_vn > expiration_date:
            try:
                os.remove(FREE_KEY_FILE)
            except:
                pass
            return False, "KEY_EXPIRED", None
    
        diff = expiration_date - now_vn
        seconds = diff.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        time_left_msg = f"Hết hạn trong {hours} giờ, {minutes} phút"
        
        return True, time_left_msg, saved_key
    except:
        try:
            os.remove(FREE_KEY_FILE)
        except:
            pass
        return False, "DATE_PARSE_ERROR", None

def print_line(char='=', length=60, color=None):
    if color is None:
        color = C.MUTED
    print(color + char * length + C.RESET)

def format_number(num):
    if num is None:
        return "-"
    if isinstance(num, (int, float)):
        return f"{num:,.4f}"
    return str(num)

def get_progress_bar(current, total, length=20):
    if total <= 0:
        return f"[{' ' * length}]"
    current = max(0, min(current, total))
    filled = int((current / total) * length)
    bar = '█' * filled + '░' * (length - filled)
    return f"[{bar}]"

def setup_session():
    s = requests.Session()
    headers = {
        'accept': '*/*', 'origin': 'https://winhash.io', 'referer': 'https://winhash.io/',
        'user-agent': 'Mozilla/5.0', 'content-type': 'application/json'
    }
    return s, headers

def get_balance(s, headers, uid, key):
    h = headers.copy(); h['user-id'] = str(uid); h['user-secret-key'] = key
    try: payload = {'user_id': int(uid), 'source': 'home'}
    except ValueError: exit_tool_with_error()
    try:
        r = s.post(API_URL_GET_BALANCE, headers=h, json=payload, timeout=10)
        d = r.json()
        if d.get('code') == 0: return d['data']['user_asset']
    except: pass
    exit_tool_with_error()

def place_Mano_bet(s, headers, uid, key, amt, asset, is_less):
    h = headers.copy(); h['user-id'] = str(uid); h['user-secret-key'] = key
    body = {
        "odds": Mano_ODDS, "num_left": Mano_NUM_LEFT, "num_right": Mano_NUM_RIGHT,
        "bet_amount": round(amt, 4), "asset": asset, "is_less_than": is_less
    }
    try:
        r = s.post(API_URL_CREATE_ORDER, headers=h, json=body, timeout=15)
        d = r.json()
        if r.status_code == 200 and d.get('code') == 0:
            g = d['data']
            return True, g.get('hit'), g.get('award_amount')-g.get('bet_amount'), g.get('num_result')
    except: pass
    return False, False, 0, 0

def calculate_mean(data):
    if not data: return 0.0
    return sum(data) / len(data)

def calculate_variance(data):
    if len(data) < 2: return 0.0
    mean = calculate_mean(data)
    return sum((x - mean) ** 2 for x in data) / len(data)

def calculate_std_dev(data):
    return math.sqrt(calculate_variance(data))

def calculate_covariance(x, y):
    if len(x) != len(y) or len(x) < 2: return 0.0
    mean_x = calculate_mean(x)
    mean_y = calculate_mean(y)
    return sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)

def calculate_correlation(x, y):
    std_dev_x = calculate_std_dev(x)
    std_dev_y = calculate_std_dev(y)
    if std_dev_x == 0 or std_dev_y == 0: return 0.0
    return calculate_covariance(x, y) / (std_dev_x * std_dev_y)

class MathematicalPredictorV1:
    def __init__(self):
        self.results = deque(maxlen=100)
        self.N_GRAM_LEN = 3
        self.n_gram_probs = {}

    def push(self, is_small):
        if len(self.results) >= self.N_GRAM_LEN:
            state = tuple(list(self.results)[-self.N_GRAM_LEN:])
            if state not in self.n_gram_probs:
                self.n_gram_probs[state] = [0, 0]
            self.n_gram_probs[state][1 if is_small else 0] += 1
        self.results.append(is_small)

    def predict(self):
        small_prob, confidence = 0.5, 0.0
        
        lt_prob, lt_conf = self.analyze_long_term_bias()
        ng_prob, ng_conf = self.analyze_sequence_bias()
        
        combined_prob = (lt_prob * lt_conf + ng_prob * ng_conf) / (lt_conf + ng_conf) if (lt_conf + ng_conf) > 0 else THEORETICAL_SMALL_PROB
        combined_conf = max(lt_conf, ng_conf)
        
        return combined_prob, combined_conf
    
    def analyze_sequence_bias(self):
        if len(self.results) < self.N_GRAM_LEN: return 0.5, 0.0
        state = tuple(list(self.results)[-self.N_GRAM_LEN:])
        if state in self.n_gram_probs:
            counts = self.n_gram_probs[state]
            total = sum(counts)
            if total >= 3:
                small_prob = counts[1] / total
                confidence = min(0.9, total / 10.0)
                return small_prob, confidence
        return 0.5, 0.3

    def analyze_long_term_bias(self):
        if len(self.results) < 20: return THEORETICAL_SMALL_PROB, 0.3
        long_small_count = sum(self.results)
        long_prob = long_small_count / len(self.results)
        recent_small_count = sum(list(self.results)[-20:])
        recent_prob = recent_small_count / 20.0
        combined_prob = (long_prob * 0.7 + recent_prob * 0.3)
        confidence = 0.65
        return combined_prob, confidence

class AdvancedStatisticsSystem:
    def __init__(self):
        self.wins = 0
        self.loses = 0
        self.bet_history = deque(maxlen=50)
        self.current_win_streak = 0
        self.current_lose_streak = 0
        self.max_win_streak = 0
        self.max_lose_streak = 0
        self.win_streaks_history = []

    def update(self, win, bet_choice, bet_amount, result_is_small, num_result):
        if win:
            self.wins += 1
            self.current_win_streak += 1
            self.current_lose_streak = 0
            if self.current_win_streak > self.max_win_streak:
                self.max_win_streak = self.current_win_streak
        else:
            self.loses += 1
            self.current_lose_streak += 1
            self.current_win_streak = 0
            if self.current_lose_streak > self.max_lose_streak:
                self.max_lose_streak = self.current_lose_streak
        
        if self.current_win_streak > 0 and win:
            self.win_streaks_history.append(self.current_win_streak)
        
        self.bet_history.append({
            'win': win, 
            'choice': bet_choice, 
            'amount': bet_amount, 
            'result_small': result_is_small, 
            'num': num_result, 
            'time': datetime.now().strftime("%H:%M:%S")
        })

    def get_stats(self):
        total = self.wins + self.loses
        rate = (self.wins / total) if total > 0 else 0
        return self.wins, self.loses, rate, self.current_win_streak, self.current_lose_streak

class DeterministicSimulator:
    def __init__(self):
        self.time_seed = int(time.time() * 1000) % 1000000
        self.counter = 0

    def generate_deterministic_number(self):
        self.counter += 1
        x = (self.time_seed + self.counter * 9301 + 49297) % 233280
        return x / 233280.0

    def simulate_result(self, predicted_small_prob, confidence):
        adjusted_prob = predicted_small_prob * (0.7 + confidence * 0.3)
        adjusted_prob = max(0.3, min(0.7, adjusted_prob))
        rand_val = self.generate_deterministic_number()
        is_small = rand_val < adjusted_prob
        if is_small:
            num = 20.0 + (Mano_NUM_LEFT - 20.0) * self.generate_deterministic_number()
        else:
            num = Mano_NUM_LEFT + (100.0 - Mano_NUM_LEFT) * self.generate_deterministic_number()
        return is_small, num

def human_ts():
    return datetime.now(tz).strftime("%H:%M:%S")

def display_status_header(stats, bal_data, profit, coin, predictor, total_games, played_games):
    clear()
    
    print()
    print_line('═', 80, C.PRIMARY)
    print(get_castorice_gradient("                 Lucky Hash - M-Tool [SangPhung]"))
    print_line('═', 80, C.PRIMARY)
    
    b = format_number(bal_data.get('BUILD'))
    u = format_number(bal_data.get('USDT'))
    
    pnl_str = f"{profit:+,.4f}"
    pnl_color = C.SUCCESS if profit >= 0 else C.ERROR
    
    wins, loses, rate, win_streak, lose_streak = stats.get_stats()
    
    key_color = C.SUCCESS if ACTIVE_KEY_TYPE == "VIP" else C.WARNING
    
    print(f"{C.INFO}║ {C.BOLD}Số Dư:{C.RESET} {b} BUILD {C.MUTED}|{C.RESET} {u} USDT {C.INFO}|{C.RESET} {C.BOLD}Lãi/Lỗ:{C.RESET} {pnl_color}{pnl_str} {coin}{C.RESET} {C.INFO}║{C.RESET}")
    print(f"{C.INFO}║ {C.BOLD}Tỉ Lệ W/L:{C.RESET} {C.SUCCESS}{wins}{C.RESET}/{C.ERROR}{loses}{C.RESET} ({C.ACCENT}{rate*100:.2f}%{C.RESET}) {C.INFO}|{C.RESET} {C.BOLD}Chuỗi:{C.RESET} {C.SUCCESS}W{win_streak}{C.RESET}/{C.ERROR}L{lose_streak}{C.RESET} {C.INFO}|{C.RESET} {C.BOLD}KEY:{C.RESET} {key_color}{ACTIVE_KEY_TYPE}{C.RESET} {C.INFO}║{C.RESET}")
    
    prob, conf = predictor.predict()
    small_percent = prob * 100
    big_percent = 100 - small_percent
    
    small_color = C.TT8_GREEN_PRIMARY if small_percent >= 50 else C.ORANGE
    big_color = C.ORANGE if big_percent > 50 else C.TT8_GREEN_PRIMARY
    
    progress = get_progress_bar(played_games, total_games, 20)
    
    print_line('-', 80, C.INFO)
    print(f"{C.INFO}║ {C.BOLD}Dự đoán:{C.RESET} {small_color}NHỎ {small_percent:.2f}%{C.RESET} {C.MUTED}|{C.RESET} {big_color}LỚN {big_percent:.2f}%{C.RESET} {C.INFO}|{C.RESET} {C.BOLD}Ván:{C.RESET} {played_games}/{total_games} {progress}{C.RESET} {C.INFO}║{C.RESET}")
    print_line('═', 80, C.PRIMARY)

def display_game_status(ui_state, choice=None, current_bet=None, coin=None, last_result_data=None):
    if ui_state == "BETTING":
        choice_text = "NHỎ (<54.12)" if choice == 1 else "LỚN (>54.12)"
        choice_color = C.TT8_GREEN_PRIMARY if choice == 1 else C.ORANGE
        bet_amt = format_number(current_bet)
        print(f"{C.SUCCESS}╔══════════════════════════════════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.SUCCESS}║{C.RESET} {C.SUCCESS}🎯 {C.BOLD}DỰ ĐOÁN: {choice_color}{choice_text:20}{C.RESET} {C.SUCCESS}║{C.RESET}")
        print(f"{C.SUCCESS}║{C.RESET} {C.INFO}💰 Đặt cược: {C.WARNING}{C.BOLD}{bet_amt} {coin}{C.RESET} {C.SUCCESS}║{C.RESET}")
        print(f"{C.SUCCESS}╚══════════════════════════════════════════════════════════════════════════════╝{C.RESET}")
    elif ui_state == "RESULT":
        if last_result_data:
            win = last_result_data['win']
            num = last_result_data['num']
            delta = last_result_data['delta']
            res_str = f"{num:.2f}"
            if win:
                print(f"{C.SUCCESS}╔══════════════════════════════════════════════════════════════════════════════╗{C.RESET}")
                print(f"{C.SUCCESS}║{C.RESET} {C.GOLD_1}🎉 {C.BOLD}WIN!{C.RESET} {C.SUCCESS}Kết quả: {res_str} {C.MUTED}|{C.RESET} {C.SUCCESS}+{delta:,.4f} {coin}{C.RESET} {C.SUCCESS}║{C.RESET}")
                print(f"{C.SUCCESS}╚══════════════════════════════════════════════════════════════════════════════╝{C.RESET}")
            else:
                print(f"{C.ERROR}╔══════════════════════════════════════════════════════════════════════════════╗{C.RESET}")
                print(f"{C.ERROR}║{C.RESET} {C.ERROR}💔 {C.BOLD}LOSE!{C.RESET} {C.ERROR}Kết quả: {res_str} {C.MUTED}|{C.RESET} {C.ERROR}{delta:,.4f} {coin}{C.RESET} {C.ERROR}║{C.RESET}")
                print(f"{C.ERROR}╚══════════════════════════════════════════════════════════════════════════════╝{C.RESET}")

def display_recent_bets(history):
    print()
    print(f"{C.INFO}--- LỊCH SỬ GẦN ĐÂY ({len(history)}/{history.maxlen}) ---{C.RESET}")
    if not history:
        print(f"{C.MUTED}Chưa có ván nào.{C.RESET}")
        return
        
    for item in list(history)[::-1]:
        win = item['win']
        choice = item['choice']
        amount = format_number(item['amount'])
        num = f"{item['num']:.2f}"
        
        status_color = C.SUCCESS if win else C.ERROR
        status_icon = "W" if win else "L"
        choice_text = "NHỎ" if choice == 1 else "LỚN"
        
        print(f"{C.MUTED}[{item['time']}]{C.RESET} {status_color}[{status_icon}]{C.RESET} {C.PRIMARY}{choice_text}{C.RESET} {C.ACCENT}{amount}{C.RESET} -> {status_color}{num}{C.RESET}")
    print_line('-', 80, C.MUTED)

def menu_input():
    clear()
    print()
    print_line('═', 80, C.PRIMARY)
    print(get_castorice_gradient("                 Lucky Hash - CẤU HÌNH [SangPhung]"))
    print_line('═', 80, C.PRIMARY)
    print()
    
    uid = input(f"{C.PRIMARY}➜ {C.BOLD}Nhập User ID: {C.CASTORICE_PRIMARY}").strip()
    key = input(f"{C.PRIMARY}➜ {C.BOLD}Nhập Secret Key: {C.CASTORICE_PRIMARY}").strip()
    coin = input(f"{C.PRIMARY}➜ {C.BOLD}Chọn loại tiền (BUILD/USDT/WORLD, mặc định BUILD): {C.CASTORICE_PRIMARY}").strip().upper() or 'BUILD'
    total_games_input = input(f"{C.PRIMARY}➜ {C.BOLD}Tổng số ván muốn chơi (mặc định 100): {C.CASTORICE_PRIMARY}").strip()
    bet_start_input = input(f"{C.PRIMARY}➜ {C.BOLD}Số tiền cược ban đầu (mặc định 10): {C.CASTORICE_PRIMARY}").strip()
    multiplier_input = input(f"{C.PRIMARY}➜ {C.BOLD}Hệ số nhân khi thua (mặc định 1.2): {C.CASTORICE_PRIMARY}").strip()
    fast_mode_input = input(f"{C.PRIMARY}➜ {C.BOLD} Cược siêu nhanh?(y/n) mặc định n): {C.CASTORICE_PRIMARY}").strip().lower()
    lose_limit_input = input(f"{C.PRIMARY}➜ {C.BOLD}Giới hạn chuỗi thua (nhập số, ví dụ 3, 0 để tắt): {C.CASTORICE_PRIMARY}").strip()
    
    print(C.RESET, end="")
    
    try: total_games = int(total_games_input) if total_games_input else 100
    except: total_games = 100
    if total_games < 1: total_games = 100
    
    try: bet_start = float(bet_start_input) if bet_start_input else 0.01
    except: bet_start = 0.01
    
    try: multiplier = float(multiplier_input) if multiplier_input else 2.0
    except: multiplier = 2.0
    
    is_fast_mode = fast_mode_input == 'y'
    
    try: max_lose_streak_limit = int(lose_limit_input) if lose_limit_input else 0
    except: max_lose_streak_limit = 0
    
    return uid, key, coin, total_games, bet_start, multiplier, is_fast_mode, max_lose_streak_limit

def main():
    global ACTIVE_KEY_TYPE
    clear()
    
    print()
    print_line('═', 80, C.PRIMARY)
    print(get_castorice_gradient("                 Lucky Hash - V1.0 [SangPhung]"))
    print_line('═', 80, C.PRIMARY)
    
    current_ip = get_ip_address()
    
    if not current_ip:
        exit_tool_with_error()
    
    key_found = False
    final_message = ""
    saved_key_used = None

    is_valid_vip, msg_vip, saved_key_vip = check_local_donate_key(current_ip)
    
    if is_valid_vip:
        ACTIVE_KEY_TYPE = "VIP"
        final_message = msg_vip
        saved_key_used = saved_key_vip
        key_found = True
    
    if not key_found:
        is_valid_free, msg_free, saved_key_free = kiem_tra_ip_free(current_ip)
        if is_valid_free:
            ACTIVE_KEY_TYPE = "FREE"
            final_message = f"Key Free Hợp lệ! Còn lại: {msg_free}"
            saved_key_used = saved_key_free
            key_found = True

    if not key_found:
        expected_key, expected_expiry_date = generate_key_and_url(current_ip)
        save_local_free_key(expected_key, expected_expiry_date)
        
        is_valid_free_new, msg_free_new, saved_key_free_new = kiem_tra_ip_free(current_ip)

        if is_valid_free_new:
            ACTIVE_KEY_TYPE = "FREE"
            final_message = f"Key Free (Mới) Hợp lệ! Còn lại: {msg_free_new}"
            saved_key_used = saved_key_free_new
            key_found = True

    if not key_found:
        exit_tool_with_error()
    
    print(f"\n{C.SUCCESS}Key {ACTIVE_KEY_TYPE} Hợp lệ!{C.RESET}")
    print(f"{C.SUCCESS}{final_message}{C.RESET}")
    time.sleep(2)
            
    uid, key, coin, total_games, bet_start, multiplier, is_fast_mode, max_lose_streak_limit = menu_input()
    
    predictor = MathematicalPredictorV1()
    statistics = AdvancedStatisticsSystem()
    simulator = DeterministicSimulator()
    wins = loses = 0
    profit = 0.0
    s, headers = setup_session()
    
    current_bet = bet_start
    played_games = 0
    
    try:
        while played_games < total_games:
            played_games += 1
            
            bal_data = get_balance(s, headers, uid, key)
            
            if not bal_data or bal_data.get(coin, 0) < current_bet:
                exit_tool_with_error()
                
            if max_lose_streak_limit > 0 and statistics.current_lose_streak >= max_lose_streak_limit:
                exit_tool_with_error()
                
            prob, conf = predictor.predict()
            
            choice = 1 if prob >= 0.50 else 0
            
            display_status_header(statistics, bal_data, profit, coin, predictor, total_games, played_games)
            display_game_status("BETTING", choice, current_bet, coin)
            display_recent_bets(statistics.bet_history)
            
            time.sleep(1)
            
            ok = hit = delta = num = 0
            
            if not is_fast_mode:
                ok, hit, delta, num = place_Mano_bet(s, headers, uid, key, current_bet, coin, choice)
                win = hit
            else:
                is_small, num = simulator.simulate_result(prob, conf)
                win = (choice == 1 and is_small) or (choice == 0 and not is_small)
                delta = current_bet * (Mano_ODDS - 1) if win else -current_bet
                ok = True
            
            if not ok:
                time.sleep(1)
                played_games -= 1
                exit_tool_with_error()
                
            is_small_res = (num <= Mano_NUM_LEFT)
            predictor.push(is_small_res)
            
            profit += delta
            statistics.update(win, choice, current_bet, is_small_res, num)
            
            last_res = {'win': win, 'num': num, 'delta': delta}
            
            display_status_header(statistics, bal_data, profit, coin, predictor, total_games, played_games)
            display_game_status("RESULT", choice, current_bet, coin, last_res)
            display_recent_bets(statistics.bet_history)
            
            if win:
                current_bet = bet_start
            else:
                current_bet = current_bet * multiplier
                
            if not is_fast_mode:
                time.sleep(3)
            else:
                time.sleep(0.1)

    except KeyboardInterrupt:
        os.system("cls" if os.name == "nt" else "clear")
        print_line('═', 80, C.PRIMARY)
        print(f"{C.WARNING}KẾT THÚC PHIÊN. TỔNG Lãi/Lỗ: {C.SUCCESS}{profit:,.4f} {coin}{C.RESET}")
        print_line('═', 80, C.PRIMARY)
        sys.exit(0)
    except Exception as e:
        exit_tool_with_error()
    finally:
        print_line('═', 80, C.PRIMARY)
        print(f"{C.WARNING}KẾT THÚC PHIÊN. TỔNG Lãi/Lỗ: {C.SUCCESS}{profit:,.4f} {coin}{C.RESET}")
        print_line('═', 80, C.PRIMARY)
        time.sleep(5)
        sys.exit(0)

if __name__ == "__main__":
    main()
