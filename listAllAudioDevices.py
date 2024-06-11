import pyaudio

p = pyaudio.PyAudio()

for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    device_name = info['name'].encode('latin1').decode('utf-8')
    print(f"Device {i}: {device_name}")

p.terminate()
