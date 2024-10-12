import os
import sys
import tkinter
from tkinter import *
from PIL import ImageTk, Image
import requests

def resource_path(relative_path): # PyInstaller 절대경로 호출용
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class VTuberLiveStatus:
    def __init__(self, root):
        self.root = root
        self.root.title("StelLive Live Status")
        self.root.geometry("965x480+100+100") # 창 크기
        self.root.resizable(True, True) # 창 조절 가능한지

        self.image_list = [ # 이미지 경로
            "stellive_image/1_Kanna.png",
            "stellive_image/2_Yuni.png",
            "stellive_image/3_Hina.png",
            "stellive_image/4_Mashiro.png",
            "stellive_image/5_Rize.png",
            "stellive_image/6_Tabi.png",
            "stellive_image/7_Shibuki.png",
            "stellive_image/8_Rin.png",
            "stellive_image/9_Nana.png",
            "stellive_image/10_Riko.png"
        ]

        self.stelNameList = [ # 스텔 이름 리스트
            "아이리 칸나", "아야츠노 유니", "시라유키 히나", 
            "네네코 마시로", "아카네 리제", "아라하시 타비", 
            "텐코 시부키", "아오쿠모 린", "하나코 나나", "유즈하 리코"
        ]

        self.channel_ids = [ # 치지직 채널 ID
            'f722959d1b8e651bd56209b343932c01',  # 칸나
            '45e71a76e949e16a34764deb962f9d9f',  # 유니
            'b044e3a3b9259246bc92e863e7d3f3b8',  # 히나
            '4515b179f86b67b4981e16190817c580',  # 마시로
            '4325b1d5bbc321fad3042306646e2e50',  # 리제
            'a6c4ddb09cdb160478996007bff35296',  # 타비
            '64d76089fba26b180d9c9e48a32600d9',  # 시부키
            '516937b5f85cbf2249ce31b0ad046b0f',  # 린
            '4d812b586ff63f8a2946e64fa860bbf5',  # 나나
            '8fd39bb8de623317de90654718638b10'   # 리코
        ]

        self.labels = []  # 각 상태 레이블을 저장하기 위한 리스트

        self.headers = { # 치지직이 뱉기 때문에 헤더에 UA 넣어서 보내야함
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }
        self.chzzk_url = 'https://api.chzzk.naver.com/service/v1/channels/{channelID}'

        self.setup_grid()
        self.load_images_and_status()
        self.update_status()  # 초기 상태 업데이트 호출

    def setup_grid(self): # 고정 안하면 글자 ㅈㄴ 이상하게 나옴
        self.root.grid_columnconfigure(0, minsize=80)  # 이미지 열의 고정 크기
        self.root.grid_columnconfigure(1, minsize=80)  # 이름 열의 고정 크기
        self.root.grid_columnconfigure(2, minsize=120)  # 상태 열의 고정 크기

    def load_images_and_status(self): # 이미지랑 상태 로딩하는 메인 부분
        for i, image in enumerate(self.image_list): # for 대신에 쓴다는건 아는데 뭔소린지 이해가 더 필요
            frame = Frame(self.root)
            # frame.grid(row=i, column=0, padx=5, pady=0) # 원래 쓰던 세로로 된 것
            frame.grid(row=i // 2, column=i % 2, padx=5, pady=5)  # 그리드 배치 변경
            # 위 코드로 가로로 나눠서 출력을 함

            # 이미지 로드 하는 부분
            open_image = Image.open(resource_path(image))
            chara_image = open_image.resize((80, 80))
            chara_image = ImageTk.PhotoImage(chara_image)

            chara_label = Label(frame, image=chara_image, width=80)
            chara_label.grid(row=0, column=0, padx=5)
            chara_label.image = chara_image

            # 스텔라이브 캐릭터 이름 화면 출력
            name_label = Label(frame, text=self.stelNameList[i], font=('Pretendard JP Variable', 20), width=9, anchor="w")
            name_label.grid(row=0, column=1, padx=10)

            # 라이브 현황 화면 출력
            status_label = Label(frame, text="", font=('Pretendard JP Variable', 20), width=11, anchor="w")
            status_label.grid(row=0, column=2, padx=10)
            self.labels.append(status_label)  # Append status label to list

    # 라이브 정보 가져오기
    def update_status(self):
        for i, channel_id in enumerate(self.channel_ids):
            url = self.chzzk_url.format(channelID=channel_id)
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:  # 성공적으로 수신했을 때
                data = response.json() # HTML 말고 JSON으로 해야함
                open_live_status = data['content']['openLive']
                if open_live_status:
                    status_text = "📺 지금 방송 중!"
                else:
                    status_text="❌ 방송 중 아님!"
            else:
                status_text = "상태 확인 실패!"

            self.labels[i].config(text=status_text)  # 프로그램의 라이브 현황 갱신

        self.root.after(30000, self.update_status)  # 30초 후 다시 상태 업데이트

if __name__ == '__main__':
    root = tkinter.Tk()
    app = VTuberLiveStatus(root)
    root.mainloop()