from data_structures import ChainingHashTable
from duty_engine import is_date_in_range


def global_filter(date_hash, date_list, exceptions):
    #1. 전역자 필터링: 
    #2. 열외 명단(exception_list) 필터링:
    exception_list = []
    for e in exceptions:
        exp_info = (e['군번'], e['시작일'], e['종료일'], e['사유'])
        exception_list.append(exp_info)

    print(exception_list)
    for day in date_list:
        today_duty = date_hash.get(day)
        for exp_worker in exception_list:
            id_tag, from_date, to_date, exp_type = exp_worker
            if is_date_in_range(day, from_date, to_date):
                today_duty.get(exp_type).append(id_tag)


# ---------------------------------------------------------
# CASE 3. 날짜별 보직 활성화 체크
# 목적: 특정 근무가 없는 날 (식기 없는 날, 훈련) 근무 제외
# ---------------------------------------------------------

def date_duty_filter(day, duty_type):
    """
    - 근무 공정표 보니 1월에 2회 식기 없는 날 존재
    - 단체로 훈련 나가는 날 특정 근무 없음 
    """
    pass
