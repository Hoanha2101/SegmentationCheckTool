from library import *
from utils import AI
from set_up import *

# Load video
video = cv2.VideoCapture(video_path)

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ
screen_width = 1536
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("CHECK SEGMENTATION")
font = pygame.font.Font(None, 30)

# Tốc độ tua ngược (số frame)
REWIND_FRAMES = 30

# Vẽ nút tua ngược
rewind_path = os.path.join("./image/left_re.png")
rewind_surface = pygame.image.load(rewind_path)
rewind_surface = pygame.transform.scale(rewind_surface, (50, 50))
rewind_surface_area = pygame.Rect(1310,600, 50, 50)

# Vẽ nút pause
pause_path = os.path.join("./image/pause-button.png")
pause_surface = pygame.image.load(pause_path)
pause_surface = pygame.transform.scale(pause_surface, (50, 50))
pause_surface_area = pygame.Rect(1385,600, 50,50)

# Vẽ nút play
play_path = os.path.join("./image/play-button.png")
play_surface = pygame.image.load(play_path)
play_surface = pygame.transform.scale(play_surface, (50, 50))
play_surface_area = pygame.Rect(1385,600, 50,50)

# Vẽ nút tua tới
Fast_forward_rewind_path = os.path.join("./image/right_re.png")
Fast_forward_rewind_surface = pygame.image.load(Fast_forward_rewind_path)
Fast_forward_rewind_surface = pygame.transform.scale(Fast_forward_rewind_surface, (50, 50))
Fast_forward_rewind_surface_area = pygame.Rect(1460,600, 50,50)

#nút capture
camera_icon_path = os.path.join("./image/camera.png")
camera_icon_surface = pygame.image.load(camera_icon_path)
camera_icon_surface = pygame.transform.scale(camera_icon_surface, (50, 50))
camera_icon_surface_area = pygame.Rect(1385, 700, 50,50)

#title original image folder
title_original_image_folder_color = (255,0,0)
title_original_image_folder_text = font.render("ORIGINAL", True, title_original_image_folder_color)
title_original_image_folder_rect = title_original_image_folder_text.get_rect(center=(1358, 40))

#name file - folder original image
image_name_color = (0,200,0)
image_name_color_font = pygame.font.Font(None, 26)
image_name_text = image_name_color_font.render("-", True, image_name_color)
image_name_rect = image_name_text.get_rect(center=(1311, 80))

#title segmentation image folder
title_segmentation_image_folder_color = (255,0,0)
title_segmentation_image_folder_text = font.render("SEGMENTATION", True, title_segmentation_image_folder_color)
title_segmentation_image_folder_rect = title_segmentation_image_folder_text.get_rect(center=(1390, 300))

#name file - folder seg image
image_name_seg_color = (0,200,0)
image_name_seg_color_font = pygame.font.Font(None, 26)
image_name_seg_text = image_name_seg_color_font.render("-", True, image_name_seg_color)
image_name_seg_rect = image_name_seg_text.get_rect(center=(1311, 80))

#name file - folder original image
image_seg_name_color = (0,200,0)
image_seg_name_color_font = pygame.font.Font(None, 26)
image_seg_name_text = image_seg_name_color_font.render("-", True, image_seg_name_color)
image_seg_name_rect = image_seg_name_text.get_rect(center=(1310, 350))

# Hàm chụp ảnh, lấy trực tiếp frame từ video
def capture_sample():
    ret, frame = video.read()
    folder_path = "./original_data"
    if ret:
        item_count = len(os.listdir(folder_path))
        sample_image = "original_" + str(item_count + 1) + ".jpg"
        path_sample_image = folder_path + "/"+ sample_image
        cv2.imwrite(path_sample_image,frame)

# Trạng thái của video (True - đang phát, False - tạm dừng)
is_playing = True
mask_frame = None
S = True #Biến công tắt khi sử dụng Pause để cố định frame lúc dừng 
is_capture = False
is_capture_segment = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        # Sử dụng chuột để thao tác
        elif event.type == MOUSEBUTTONDOWN:
            # Kiểm tra xem có nhấn vào nút tua ngược không
            if rewind_surface_area.collidepoint(event.pos):
                for _ in range(REWIND_FRAMES):
                    video.set(cv2.CAP_PROP_POS_FRAMES, video.get(cv2.CAP_PROP_POS_FRAMES) - 10)
            
            if Fast_forward_rewind_surface_area.collidepoint(event.pos):
                for _ in range(REWIND_FRAMES):
                    video.set(cv2.CAP_PROP_POS_FRAMES, video.get(cv2.CAP_PROP_POS_FRAMES) + 10)

            if pause_surface_area.collidepoint(event.pos):
                is_playing = not is_playing
            
            if camera_icon_surface_area.collidepoint(event.pos):
                is_capture_segment = True
                capture_sample()
        
        #Sử dụng nút từ bàn phím     
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                for _ in range(REWIND_FRAMES):
                    video.set(cv2.CAP_PROP_POS_FRAMES, video.get(cv2.CAP_PROP_POS_FRAMES) - 5)
            
            if event.key == K_RIGHT:
                for _ in range(REWIND_FRAMES):
                    video.set(cv2.CAP_PROP_POS_FRAMES, video.get(cv2.CAP_PROP_POS_FRAMES) + 5)

            if event.key == K_SPACE:
                is_playing = not is_playing
            
            if event.key == K_RETURN:
                is_capture_segment = True
                capture_sample()
                
                
            if event.key == K_ESCAPE:
                running = False
                
    screen.fill((220,220,220))
    
    #show last name image in sample_data folder
    len_sample_folder = len(os.listdir("./original_data"))
    if len_sample_folder > 0:
        name_ = "original_" + str(len_sample_folder) + ".jpg"
        image_name_text = image_name_color_font.render(name_, True, image_name_color)
        
        captured_image_surface = pygame.image.load(os.path.join("./original_data",name_))
        original_image_width, original_image_height = captured_image_surface.get_size()
        
        captured_image_surface = pygame.transform.scale(captured_image_surface, (int(original_image_width / 9), int(original_image_height /9)))
        screen.blit(captured_image_surface,(1310, 100))
        
    screen.blit(image_name_text, image_name_rect)
    screen.blit(title_original_image_folder_text, title_original_image_folder_rect)
    
    #Đính 2 nút tua
    screen.blit(rewind_surface,(1310,600))
    screen.blit(Fast_forward_rewind_surface,(1460,600))
    
    # Đính nút pause
    if is_playing:
        screen.blit(pause_surface,(1385,600))
    else:
        screen.blit(play_surface,(1385,600))
    
    #Đính nút capture
    screen.blit(camera_icon_surface,(1385,700))

    # Đọc và hiển thị frame hiện tại (nếu đang phát)
    if is_playing:
        S = True
        ret, frame = video.read()  
    
    #Nút pause = False
    if not is_playing:
        if S:
            ret, frame = video.read()
            mask_frame = frame
            S = False
        frame = mask_frame
    
    # Định dạng lại frame show để có thể show lên pygame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = AI(frame)
    
    # Chụp ảnh segmentation
    
    path_seg = "./segmentation_data"
    if is_capture_segment:
        len_seg_folder = len(os.listdir(path_seg))
        name_seg = "segmentation_" + str(len_seg_folder + 1) + ".jpg"
        path_seg_name = os.path.join(path_seg, name_seg)
        frame_seg_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imwrite(path_seg_name,frame_seg_RGB)
        
        is_capture_segment = False
        
    len_seg_folder = len(os.listdir(path_seg))
    if len_seg_folder > 0:
        name_seg_ = "segmentation_" + str(len_seg_folder) + ".jpg"
        image_seg_name_text = image_name_color_font.render(name_seg_, True, image_seg_name_color)
        captured_image_seg_surface = pygame.image.load(os.path.join("./segmentation_data",name_seg_))
        original_image_seg_width, original_image_seg_height = captured_image_seg_surface.get_size()
        
        captured_image_seg_surface = pygame.transform.scale(captured_image_seg_surface, (int(original_image_seg_width / 9), int(original_image_seg_height /9)))
        screen.blit(captured_image_seg_surface,(1310, 370))
        
    screen.blit(image_seg_name_text, image_seg_name_rect)
    screen.blit(title_segmentation_image_folder_text, title_segmentation_image_folder_rect)
     
    frame = cv2.resize(frame, (1280, 720))
    frame = cv2.flip(frame, 1)
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame = pygame.surfarray.make_surface(frame) 
    
    screen.blit(frame, (10, 30))  
    
    pygame.display.flip()

# Đóng video và Pygame
video.release()
pygame.quit()
