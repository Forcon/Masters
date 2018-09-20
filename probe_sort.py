import numpy as np

img = ('img_1','img_2','img_3','img_4', 'img_5', 'img_6', 'img_7')
autor = ('Masya', 'Forcon', 'Forcon', 'Forcon', 'Alex', 'Tupsya', 'Tupsya')
score = (1, 5, 2, 3, 7, 4, 6)
len_user = (1, 3, 3, 3, 1, 2, 2)



# a = np.array([[1,2,1],[4,5,6],[0,0,1],[0,0,3],[0,0,2],[0,0,2]])

ind = np.lexsort((img, autor, score, len_user))

# b = np.sort(a.view('i8,i8,i8'), order=['f1'])#.view(np.int)

rez = [(img[i], autor[i], score[i]) for i in ind]

image = [(img[i]) for i in ind]
aut = [(autor[i]) for i in ind]
fav = [(score[i]) for i in ind]

print(rez)
print('\n')
print(list(reversed(image)))
print(list(reversed(aut)))
print(list(reversed(fav)))
# print('\n')
# print(b)
# array([[0, 0, 1],
#        [1, 2, 3],
#        [4, 5, 6]])
