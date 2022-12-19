# tkSliderWidget (Application: Life Satisfaction)
Implementation of a slider widget using tkinter, multiple slider supported

for an example see:
`main.py`

Initial Position 
![life_sat_scale_ogpos](https://user-images.githubusercontent.com/88394968/208348326-496d9976-6054-46d7-925a-7e6ee3b7891e.JPG)

After User Input
![life_sat_scale_check](https://user-images.githubusercontent.com/88394968/208348391-1ddc701a-7ef3-4ffd-8486-63e54e889c59.JPG)


```python
	
import tkinter as tk
from tkSliderWidget import Slider

root = tk.Tk()
life_sat=tk.StringVar()
life_sat = life_sat.set("")

slider = Slider(root, width = 500, height = 500, min_val = 0, max_val = 10, init_lis = [1,2,3,4,5,6,7,8,9], show_value = TRUE)
name_label = tk.Label(root, text = 'My current life satisfaction is: (out of 10)', font=('calibre',10, 'bold'))
entry = tk.Entry(root, textvariable = life_sat, font=('calibre',10,'normal'))
l3 = Label(root, text = "Life Satisfaction Scale")
b1 = Button(root, text ="Done")

name_label.pack()
entry.pack()
slider.pack()
l3.pack(anchor=CENTER)
b1.pack(anchor=CENTER)
# optionally add a callback on value change
slider.setValueChageCallback(lambda vals: print(vals))

root.title("Slider Widget")
root.mainloop()

print(slider.getValues())

```
