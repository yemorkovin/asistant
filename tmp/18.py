import win32com.client
speaker = win32com.client.Dispatch("SAPI.SpVoice")

speaker = speaker.GetVoices()
print(speaker)