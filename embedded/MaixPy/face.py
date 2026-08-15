import sensor, image, lcd, time
import KPU as kpu
# LCD
lcd.init()

# Kamera
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)

sensor.set_auto_whitebal(True)
sensor.set_auto_gain(True)
sensor.set_auto_exposure(True)

sensor.set_saturation(2)
sensor.set_contrast(1)
sensor.set_brightness(1)
sensor.set_vflip(1)      # bazı boardlarda stabilite artırır
sensor.set_hmirror(1)    # opsiyonel

sensor.skip_frames(time=2000)

clock = time.clock()

# Face detect model yükle
task = kpu.load("/sd/facedetect.kmodel")

# YOLO ayarları (çok önemli)
anchor = (1.889, 2.5245, 2.9465, 3.94056,
          3.99987, 5.3658, 5.155437, 6.92275,
          6.718375, 9.01025)

a = kpu.init_yolo2(task, 0.1, 0.4, 5, anchor)

print("Face detect hazır")

while True:
    clock.tick()
    img = sensor.snapshot()

    code = kpu.run_yolo2(task, img)

    if code:
        for i in code:
            img.draw_rectangle(i.rect(), color=(255,0,0))
            img.draw_string(i.x(), i.y(), "Face", color=(0,255,0))

    lcd.display(img)
    print("FPS:", clock.fps())
    print(sensor.get_id())
    print(sensor.width(), sensor.height())
