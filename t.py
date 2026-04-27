
import os
import sys
import subprocess
import random



try:
    import pygame
except ImportError:
    print("Pygame chưa được cài. Đang mở CMD để cài đặt...")
    subprocess.call('start cmd /k "pip install pygame"', shell=True)
    print("Sau khi cài xong, chạy lại chương trình.")
    sys.exit()

pygame.init()

# Kích thước cửa sổ
RONG, CAO = 960, 540
man_hinh = pygame.display.set_mode((RONG, CAO))
pygame.display.set_caption("Vì yêu cứ đâm đầu")

# Nhạc nền
co_nhac = os.path.exists("song.mp3")
if co_nhac:
    pygame.mixer.init()
    pygame.mixer.music.load("song.mp3")
    pygame.mixer.music.play(-1)
else:
    print("Không tìm thấy file nhạc. Chạy không có nhạc.")

# Màu sắc
HONG   = (255, 160, 220)
XAM    = (200, 200, 200)
TRANG  = (255, 255, 255)
DEN    = (0, 0, 0)

# Nền đen
nen = pygame.Surface((RONG, CAO))
nen.fill(DEN)

# Hạt bay
hat = []
for _ in range(80):
    x = random.randint(0, RONG)
    y = random.randint(0, CAO)
    toc_do = random.uniform(0.2, 0.6)
    ban_kinh = random.randint(1, 3)
    hat.append([x, y, toc_do, ban_kinh])

def cap_nhat_hat():
    for h in hat:
        h[1] -= h[2]
        if h[1] < 0:
            h[0] = random.randint(0, RONG)
            h[1] = CAO
            h[2] = random.uniform(0.2, 0.6)
            h[3] = random.randint(1, 3)
        pygame.draw.circle(man_hinh, TRANG, (int(h[0]), int(h[1])), h[3])


co_anh = os.path.exists("image.png")
if co_anh:
    anh = pygame.image.load("image.png").convert_alpha()
    ty_le = 0.17
    anh = pygame.transform.smoothscale(
        anh,
        (int(anh.get_width() * ty_le),
         int(anh.get_height() * ty_le))
    )
    hinh_rect = anh.get_rect(center=(RONG - 230, CAO // 2 - 40))

    
    mo_vien = pygame.Surface(anh.get_size(), pygame.SRCALPHA)
    do_rong_mo = int(anh.get_width() * 0.18)
    for x in range(anh.get_width()):
        khoang_cach = min(x, anh.get_width() - x - 1)
        alpha = int(255 * (khoang_cach / do_rong_mo)) if khoang_cach < do_rong_mo else 255
        pygame.draw.line(mo_vien, (255, 255, 255, alpha), (x, 0), (x, anh.get_height()))
    anh.blit(mo_vien, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

   
    phan_chieu = pygame.transform.flip(anh, False, True)
    chieu_cao_phan_chieu = int(anh.get_height() * 0.6)
    phan_chieu = pygame.transform.smoothscale(phan_chieu, (anh.get_width(), chieu_cao_phan_chieu))

    mo_phan_chieu = pygame.Surface(phan_chieu.get_size(), pygame.SRCALPHA)
    for y in range(chieu_cao_phan_chieu):
        alpha = int(180 * (1 - y / chieu_cao_phan_chieu))
        pygame.draw.line(mo_phan_chieu, (255, 255, 255, alpha), (0, y), (phan_chieu.get_width(), y))
    phan_chieu.blit(mo_phan_chieu, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
else:
    anh = None
    phan_chieu = None
    print("Không tìm thấy ảnh. Sẽ không hiển thị ảnh.")

# Font
font_tieu_de = pygame.font.Font("Oswald-VariableFont_wght.ttf", 68)
font_ca_si   = pygame.font.Font("Licorice-Regular.ttf", 36)
font_loi     = pygame.font.Font("Pacifico-Regular.ttf", 29)


tieu_de_text = "DẠO BƯỚC HONGKONG 1999"
ten_ca_si = "Cre: DP"
 
loi_bai_hat = [
"Thương MT của mk lém , rồi một ngày giông gió tóc cậu rối bời",
"Mk sẽ là người xuất hiện giúp MT buộc hết đóng muộn phiền nhaa"
]
thoi_gian_loi = [0.0, 1.5, 2.8, 7.0, 9.0, 219.5]
fade_loi = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
giu_loi  = [300.0, 300.0, 300.0, 300.0, 300.0, 300,0]

tieu_de = font_tieu_de.render(tieu_de_text, True, HONG)
ca_si   = font_ca_si.render(ten_ca_si, True, TRANG)


def hien_loi(dong1, dong2, tg_hien, fade_time, hold_time):
    x = 70
    y1 = 300
    y2 = 350
    xuat_hien = 0.5

    alpha = 255
    if tg_hien < xuat_hien:
        alpha = int(255 * (tg_hien / xuat_hien))
    elif tg_hien > xuat_hien + hold_time:
        tien_do_fade = min(1, (tg_hien - xuat_hien - hold_time) / fade_time)
        alpha = int(255 * (1 - tien_do_fade))

    def ve_dong(text, y_offset):
        mat = pygame.Surface((RONG, 60), pygame.SRCALPHA)
        bieu = font_loi.render(text, True, XAM)
        bieu.set_alpha(alpha)
        mat.blit(bieu, (x, 0))
        man_hinh.blit(mat, (x, y_offset))

    ve_dong(dong1, y1)
    ve_dong(dong2, y2)

# Vòng lặp chính 
dang_chay = True
dong_ho = pygame.time.Clock()

while dang_chay:
    man_hinh.blit(nen, (0, 0))
    cap_nhat_hat()

    if anh:
        man_hinh.blit(anh, hinh_rect)
        man_hinh.blit(phan_chieu, (hinh_rect.left, hinh_rect.bottom - 5))

    if co_nhac:
        tg_hien_tai = pygame.mixer.music.get_pos() / 1000.0
    else:
        tg_hien_tai = pygame.time.get_ticks() / 1000.0

    man_hinh.blit(tieu_de, (70, 90))
    man_hinh.blit(ca_si, (140, 170))

    for i in range(0, len(loi_bai_hat), 2):
        chi_so = i // 2
        if chi_so < len(thoi_gian_loi):
            delay = thoi_gian_loi[chi_so]
            fade = fade_loi[chi_so]
            hold = giu_loi[chi_so]
            tg = tg_hien_tai - delay
            if 0 <= tg <= 0.5 + hold + fade:
                dong2 = loi_bai_hat[i+1] if i+1 < len(loi_bai_hat) else ""
                hien_loi(loi_bai_hat[i], dong2, tg, fade, hold)

    pygame.display.flip()
    dong_ho.tick(30)

    for su_kien in pygame.event.get():
        if su_kien.type == pygame.QUIT:
            dang_chay = False

    if tg_hien_tai >= thoi_gian_loi[-1] + 6:
        dang_chay = False

pygame.quit()
sys.exit()
