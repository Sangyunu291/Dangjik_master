import csv
import calendar
from datetime import date

#--- [자료구조 정의] ---
# 1. 원형 리스트 및 포인터 정의
class Circular_List:
    def __init__(self):
        self.__c_list = []

    def append(self, x):
        self.__c_list.append(x)

    def get_at(self, idx):
        if len(self.__c_list) == 0: return None
        idx = idx % len(self.__c_list)
        return self.__c_list[idx]

    def length(self):
        return len(self.__c_list)

class List_Pointer:
    def __init__(self, p_list: Circular_List, idx):
        self.__idx = idx
        self.__p_list = p_list

    def get_val(self):
        temp = self.__p_list.get_at(self.__idx)
        self.__idx += 1
        return temp

# 2. 체이닝 해시 테이블 정의
class ChainingHashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def _hash_function(self, key):
        return hash(key) % self.size

    def set(self, key, value):
        index = self._hash_function(key)
        bucket = self.table[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def get(self, key):
        index = self._hash_function(key)
        bucket = self.table[index]
        for k, v in bucket:
            if k == key:
                return v
        return None

    def print_table(self):
        """해시 테이블 출력"""
        for c_list in self.table:
            for x in c_list :
                k, v = x
                print(f"key:{k}, value:{v}")

# --- [로직 보조 함수 ] ---

#마지막 근무자 군번 찾기
def get_start_index(c_list, last_sn):
    for i in range(c_list.length()):
        if c_list.get_at(i) == last_sn:
            return i + 1
    return 0 # 못 찾으면 처음부터

#당일 근무에 투입 안된 인원 추출
def get_next_available(ptr, assigned_set):
    while True:
        sn = ptr.get_val()
        if sn not in assigned_set:
            assigned_set.add(sn)
            return sn



# CSV 결과 출력 기능 (군번 -> 이름 변환 적용)
def get_name(sn):
    if sn == "72사단": return sn
    info = worker_info_map.get(sn)
    return info['이름'] if info else sn

# 여러 명일 경우 (예: 식기 3명) 처리용
def get_names(sn_list_str):
    if "72사단" in sn_list_str: return sn_list_str
    sns = sn_list_str.split(', ')
    return ", ".join([get_name(sn) for sn in sns])


# --- [메인 로직 실행] ---

# 1. 데이터 로드 및 정보 매핑

worker_data = []
worker_info_map = ChainingHashTable(60)
with open('./database.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        worker_data.append(row)
        worker_info_map.set(row['군번'], row)





# 2. 인원 분류 및 원형 리스트 생성
worker_data.sort(key=lambda x: x['전입일'])
mid = len(worker_data) // 2
c_list_all = Circular_List()
for w in worker_data: c_list_all.append(w['군번'])
c_list_sr = Circular_List()
for w in worker_data[:mid]: c_list_sr.append(w['군번'])
c_list_jr = Circular_List()
for w in worker_data[mid:]: c_list_jr.append(w['군번'])

# 3. 마지막 근무자 입력 및 포인터 설정
print("--- 마지막 근무자 군번을 입력하세요 (없으면 엔터) ---")
last_sub = input("위병부조장 마지막 인원: ")
last_sr = input("선임초병 마지막 인원: ")
last_jr = input("후임초병 마지막 인원: ")
last_dish = input("식기 마지막 인원 (3명 중 가장 마지막): ")

ptr_sub_guard = List_Pointer(c_list_all, get_start_index(c_list_all, last_sub))
ptr_sr_sentinel = List_Pointer(c_list_sr, get_start_index(c_list_sr, last_sr))
ptr_jr_sentinel = List_Pointer(c_list_jr, get_start_index(c_list_jr, last_jr))
ptr_dish = List_Pointer(c_list_all, get_start_index(c_list_all, last_dish))

# 4. 배정 시작
print("\n배정 년/월 입력 (예: 2026 1):")
year, month = map(int, input().split())
date_list = [day.strftime("%m-%d") for week in calendar.Calendar().monthdatescalendar(year, month) for day in week if day.month == month]


date_hash = ChainingHashTable(40)
dish_skip_count = 0

# 문자열에서 리스트로 수정
for day in date_list:
    today_duty = ChainingHashTable(10)
    today_duty.set("열외", [])
    today_duty.set("위병부조장", [])
    today_duty.set("초병_오전", [])
    today_duty.set("초병_오후", [])
    today_duty.set("식기", [])
    date_hash.set(day, today_duty)


# 열외자 리스트 구성
ot_schedule_list = []
for worker in worker_data:
    if worker['열외일정'] != 'None':
        ot_schedule_list.append(worker)


def is_date_in_range(target, start, end): return (start <= target) and (target <= end)

#해시 테이블에 열외자 추가
for day in date_list:
    for worker in ot_schedule_list:
        start, end = worker['열외일정'].split('~')
        if is_date_in_range(day, start, end):
            date_hash.get(day).get('열외').append(worker['군번'])
    
 
for day in date_list:
    assigned_today = set() # 중요: 당일 중복 방지용 셋
    ot_schedule_set = set() #당일 열외일정 집합 

    today_duty = date_hash.get(day) 

    for x in today_duty.get('열외'): ot_schedule_set.add(x)
    assigned_today = assigned_today.union(ot_schedule_set) #당일 근무자, 열외자 합집합 


    # 배정 순서: 위병부조장 -> 초병 -> 식기 (우선순위 순서대로)
    
    # 1. 위병부조장 (1명)
    today_duty.get("위병부조장").append(get_next_available(ptr_sub_guard, assigned_today))
    
    # 2. 초병 (오전/오후 각 2명)
    sn_sr_am = get_next_available(ptr_sr_sentinel, assigned_today)
    sn_jr_am = get_next_available(ptr_jr_sentinel, assigned_today)
    today_duty.get("초병_오전").append(sn_sr_am)
    today_duty.get("초병_오전").append(sn_jr_am)
    
    sn_sr_pm = get_next_available(ptr_sr_sentinel, assigned_today)
    sn_jr_pm = get_next_available(ptr_jr_sentinel, assigned_today)
    today_duty.get("초병_오후").append(sn_sr_pm)
    today_duty.get("초병_오후").append(sn_jr_pm)
    
    # 3. 식기 (5일 주기)
    dish_skip_count += 1
    if dish_skip_count % 5 == 0:
        today_duty.get("식기").append('72사단')
    else:
        d1 = get_next_available(ptr_dish, assigned_today)
        d2 = get_next_available(ptr_dish, assigned_today)
        d3 = get_next_available(ptr_dish, assigned_today)
        today_duty.get("식기").append(d1)
        today_duty.get("식기").append(d2)
        today_duty.get("식기").append(d3)
    

    date_hash.set(day, today_duty)

def save_worker_by_date_csv(filename, worker_data, date_list, date_hash):
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        # 헤더: "이름/군번" + "01-01", "01-02" ...
        header = ["군번", "이름"] + date_list
        writer.writerow(header)

        for worker in worker_data:
            sn = worker['군번']
            name = worker['이름']
            row = [sn, name]

            for day in date_list:
                today_duty = date_hash.get(day)
                duty_name = "" # 기본값 (근무 없음)
                
                # 해당 날짜의 각 항목을 뒤져서 이 군번이 있는지 확인
                for duty_type in ["위병부조장", "초병_오전", "초병_오후", "식기", "열외"]:
                    if sn in today_duty.get(duty_type):
                        duty_name = duty_type
                        break
                row.append(duty_name)
            writer.writerow(row)
    print(f"저장 완료: {filename}")


def save_duty_by_date_csv(filename, date_list, date_hash):
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        # 헤더: "근무종류" + "01-01", "01-02" ...
        header = ["근무종류"] + date_list
        writer.writerow(header)

        duties = ["위병부조장", "초병_오전", "초병_오후", "식기", "열외"]
        
        for duty in duties:
            row = [duty]
            for day in date_list:
                today_duty = date_hash.get(day)
                # 군번 리스트를 이름 리스트로 변환하여 문자열로 합침
                sn_list = today_duty.get(duty)
                names = [get_name(sn) for sn in sn_list]
                row.append(", ".join(names))
            writer.writerow(row)
    print(f"저장 완료: {filename}")


save_worker_by_date_csv('근무표1.csv', worker_data, date_list, date_hash)
save_duty_by_date_csv('근무표2.csv', date_list, date_hash)