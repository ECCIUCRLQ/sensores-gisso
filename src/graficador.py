import interpreter as interpreter
import matplotlib.pyplot as plt 

interpreter.getPage()
interpreter.getData()
  
# x-coordinates of left sides of bars  
#left = [1, 2, 3, 4, 5] 
left = interpreter.getEjeX()

print left
  
# heights of bars 
#height = [1, 24, 36, 40, 5, 2] 
height = interpreter.getEjeY() 

print height
  
# labels for bars 
tick_label = ['1', '2', '4','5'] 
  
# plotting a bar chart 
plt.bar(left, height, tick_label = tick_label, 
        width = 0.8, color = ['red', 'green']) 
  
# naming the x-axis 
plt.xlabel('Hora(s)') 
# naming the y-axis 
plt.ylabel('# Detecciones') 
# plot title 
plt.title('Actividad de sensores') 
  
# function to show the plot 
plt.show() 
