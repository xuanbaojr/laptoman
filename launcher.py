import cv2

if __name__ == "__main__":
    img = cv2.imread('test/art_0.png')
    print(img)
    cv2.imshow("xuanbao", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()