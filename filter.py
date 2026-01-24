from data_structures import ChainingHashTable
from date import is_date_in_range

def global_filter(date_hash, date_list, exceptions):
    #1. 전역자 필터링: 
    #2. 열외 명단(exception_list) 필터링:
    exception_list = []
    for e in exceptions:
        exp_info = (e['군번'], e['시작일'], e['종료일'], e['사유'])
        exception_list.append(exp_info)

    for day in date_list:
        today_duty = date_hash.get(day)
        for exp_worker in exception_list:
            id_tag, from_date, to_date, exp_type = exp_worker
            if is_date_in_range(day, from_date, to_date):
                today_duty.get(exp_type).append(id_tag)


def task_filter(sn, duty_type, worker_info_map):
    #가능근무 데이터(예: '11101') 기반 필터링:
    #순서는 위병부조장,식기,불침번,초병,CCTV로 고정
    #호출함수: get_next_available()
    work_bit = worker_info_map.get(sn)['가능근무']
    return work_bit[duty_type] == '0'


