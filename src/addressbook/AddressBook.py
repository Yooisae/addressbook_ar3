from datetime import datetime 
from faker import Faker 
from tabulate import tabulate 
from tablib import Dataset 
import sys

class AddressBook:
    headers = ["이름", "전화번호", "주소", "직업", "수정한 날짜"]

    def __init__(self):
        self.address_book = []

    def _now(self):
        """ datetime_now 함수"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def table(self):
        """print_address_book()"""
        return tabulate(self.address_book, headers = self.headers, showindex=True, tablefmt="fancy_grid")

    def show(self):
        """print_address_book()"""
        print(self.table())

    def add(self, name, phone_number, address, job):
        self.address_book.append([name, phone_number, address, job, self._now()])

    def modify(self, index, name, phone_number, address, job):
        try:
            self.address_book[index] = [name, phone_number, address, job, self._now()]
        except IndexError:
            print("없는 번호 입니다.")

    def remove(self, index):
        try:
            del self.address_book[index]
        except IndexError:
            print("없는 번호 입니다.")

    def save(self, fname, type = 'csv'):
        """address_book_save_test()"""
        if type not in ['csv', 'xlsx']:
            sys.stderr.write('파일 타입은 csv 또는 xlsx 이어야 합니다.\n')
            return

        address_book_data = Dataset()
        address_book_data.headers = self.headers
        for address in self.address_book:
            address_book_data.append(address)

        filepath = fname + '.' + type

        if type == 'xlsx':
            with open(filepath, 'wb') as f:
                f.write(address_book_data.export('xlsx'))
        elif type == 'csv':
            with open(filepath, 'w') as f:
                f.write(address_book_data.export('csv'))

    def load(self, fname, type='csv'):
        """
        address_book_load_xlsx(), address_book_load_csv()
        """
        if type not in ['csv', 'xlsx']:
            sys.stderr.write('파일 타입은 csv 또는 xlsx 이어야 합니다.\n')
            return

        address_book_data = Dataset()
        address_book_data.headers = self.headers
        filepath = fname + '.' + type

        try:
            if type == 'xlsx':
                with open(filepath, 'rb') as f:
                    address_book_data.load(f, 'xlsx')
            elif type == 'csv':
                with open(filepath, 'r') as f:
                    address_book_data.load(f, 'csv')
        except FileNotFoundError:
            sys.stderr.write(f'{fname}은 존재하지 않는 파일입니다.')
            return

        self.address_book = address_book_data


class FakeAddressBook(AddressBook):
    def __init__(self):
        super().__init__() # AddressBook 의 객체가 생성이되고 이를 초기화 한다. => self.address_book
        self.fake = Faker('ko_KR')

    def _fake_person(self):
        """fake_person()"""
        # 가짜 사람 정보 생성
        return [self.fake.name(), self.fake.phone_number(), self.fake.address(), self.fake.job(), self._now()]
    
    def add_fake(self, num):
        for _ in range(num):
            self.address_book.append(self._fake_person())

def main():
    address_book = FakeAddressBook()

    while 1:
        # 메뉴 선택
        sel = input("""1)추가 2)가짜 추가 3)수정 4)삭제 5)보기 
        6)주소록 저장 7)주소록 불러오기 8)종료 > """)
        
        #동작에 맞는 메소드 실행
        if sel == '1': # 추가
            address_book.add(input("이름: "), input("전화번호: "), input("주소: "), input("직업: "))
        elif sel == '2': # 가짜 프로필 추가
            address_book.add_fake(int(input("가짜 프로필 갯수: ")))
        elif sel == '3': # 수정
            param = int(input("번호: ")), input("이름: "), input("전화번호: "), input("주소: "), input("직업: ")
            address_book.modify(*param)
        elif sel == '4': # 삭제
            address_book.remove(int(input("번호: ")))
        elif sel == '5': # 보기
            address_book.show()
        elif sel == '6': # 주소록 저장
            address_book.save(input("파일명: "), input("파일 타입(csv 또는 xlsx): "))
        elif sel == '7': # 주소록 불러오기
            address_book.load(input("파일명: "), input("파일 타입(csv 또는 xlsx): "))
        elif sel == '8': # 종료
            break
        else:
            print("잘못된 입력입니다. 다시 입력하세요.")
            continue

        

if __name__ == "__main__":
    main()