import sys

def getValue(value):
    list_, cnt = [], 1
    for v in value.split('\n'):
        if '#' in v:    # #이 있는지 확인하는 문단
            if remark_chk(v):   # 주석이 맞는지 확인
                idx = v.rfind('#')
                value = v[idx:]
                dic = {
                    'label': f'line : {cnt} => {value}',
                    'detail' : f'{value}의 번역문'
                }
                list_.append(dic)
        cnt += 1
    print(list_)


def remark_chk(text):       # 한 문장씩 주석이 있는지 확인하는 함수
    escape = True
    chk = True
    for i in list(text):
        if i in ['"', "'"]: # ', " 문장일 시 주석이 아니다.
            chk = not chk   # Switch 개념 / 문장이 닫길시 이후에 오는 #은 주석이다.
        elif i == '\\':
            escape = False
        elif not escape:    # \ 탈출문자 다음 #가 들어올시
            continue

        if i == '#' and chk:
            return True
    
    return False

if __name__ == '__main__':
    getValue(sys.argv[1])