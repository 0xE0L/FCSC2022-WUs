# Those 2 are useful to find a character of the flag, but they don't provide us at which position it is!
locDword1PostCall = [0xfff11317, 0xfff11b04, 0xfff2c3c5, 0xfff2d406, 0xfff33aac, 0xfff33e34, 0xfff39179, 0xfff39b08, 0xfff3c826, 0xfff43074, 0xfff4fa32, 0xfff57a6f, 0xfff6a491, 0xfff6e92f, 0xfff711ad, 0xfff7ee13, 0xfff819ea, 0xfff81b60, 0xfff8c899, 0xfff9b6c4, 0xfffab543, 0xfffb146d, 0xfffb5240, 0xfffbf588, 0xfffc1ad4, 0xfffc2b6f, 0xfffc5c38, 0xfffc8b00, 0xfffcac56, 0xfffd7f65, 0xfffda626, 0xfffdcf9e, 0xffff03d0, 0xffff4c82, 0xffff7930, 0xc2d, 0x19ccd, 0x1a0fb, 0x23107, 0x29d2d, 0x2d1b9, 0x30753, 0x31f22, 0x3436c, 0x35377, 0x37187, 0x4a9bd, 0x4d92d, 0x571f5, 0x5dc63, 0x71b70, 0x720d2, 0x72b09, 0x797eb, 0x7aa76, 0x7ad97, 0x7be91, 0x7f52b, 0x8b752, 0x95338, 0x9ddd0, 0x9dfc7, 0xa34c5, 0xaf62d, 0xb1f42, 0xb3412, 0xda991, 0xdd843, 0xdff7c, 0xe38a2, 0xe6aa2]
locDword2PostCall = [0xe6b1d, 0xe38d2, 0xdffb3, 0xdd8a8, 0xda9c3, 0xb344a, 0xb1f72, 0xaf65f, 0xa34fb, 0x9e000, 0x9de08, 0x95399, 0x8b7b3, 0x7f58e, 0x7bef5, 0x7adf9, 0x7aad7, 0x7981b, 0x72b41, 0x72115, 0x71ba5, 0x5dc94, 0x5722d, 0x4d963, 0x4aa1e, 0x371b9, 0x353ac, 0x343a4, 0x31f5a, 0x307b6, 0x2d1f5, 0x29d93, 0x23107, 0x1a134, 0x19d30, 0xc64, 0xffff7963, 0xffff4ce7, 0xffff0436, 0xfffdd000, 0xfffda65b, 0xfffd7f96, 0xfffcac8f, 0xfffc8b31, 0xfffc5c6c, 0xfffc2ba7, 0xfffc1b17, 0xfffbf5c1, 0xfffb5271, 0xfffb14d3, 0xfffab5a7, 0xfff9b6fc, 0xfff8c8fb, 0xfff81b97, 0xfff81a1f, 0xfff7ee78, 0xfff711e5, 0xfff6e965, 0xfff6a50e, 0xfff57ac2, 0xfff4fa67, 0xfff430d7, 0xfff3c85c, 0xfff39b3d, 0xfff391dc, 0xfff33e9a, 0xfff33ae3, 0xfff2d436, 0xfff2c42b, 0xfff11b39, 0xfff1134b]

# This one will help us find the good position of a character!
locDword1Original = [0x2d1b9, 0x720d2, 0xfff57a6f, 0xfffc1ad4, 0xe6aa2, 0xa34c5, 0x4d92d, 0xfff4fa32, 0x30753, 0xfff2c3c5, 0x7aa76, 0xffff7930, 0xdd843, 0xb1f42, 0x37187, 0xc2d, 0xdff7c, 0x8b752, 0x72b09, 0x9ddd0, 0x9dfc7, 0xda991, 0xfffda626, 0xb3412, 0xfff43074, 0x7f52b, 0xfffcac56, 0xffff03d0, 0xfff6e92f, 0xffff4c82, 0xaf62d, 0xfff11317, 0xfff39179, 0x3436c, 0xfffc2b6f, 0xfffb146d, 0x19ccd, 0x1a0fb, 0xfffab543, 0xfff8c899, 0xfff3c826, 0x71b70, 0xfffc5c38, 0xfffb5240, 0xfff81b60, 0xfff9b6c4, 0xfff39b08, 0x35377, 0x571f5, 0x7be91, 0xfff7ee13, 0x5dc63, 0xfff2d406, 0xfffd7f65, 0x7ad97, 0xfff711ad, 0x4a9bd, 0xfffc8b00, 0xfffbf588, 0x95338, 0xfff33e34, 0x31f22, 0x29d2d, 0xfffdcf9e, 0xe38a2, 0x797eb, 0xfff11b04, 0xfff33aac, 0xfff819ea, 0xfff6a491, 0x23107]

flag = [None]*71 # initialize flag array

# Do the reverse comparison as souk does
locDword2PostCall.reverse()
for i in range(0, 71):
    # calculating the char value
    char = chr(locDword2PostCall[i]-locDword1PostCall[i])

    # lookup in locDword1Original to find at which index this char should be placed in the flag!
    index = locDword1Original.index(locDword1PostCall[i])
    
    print(hex(locDword1PostCall[i]), "|", hex(locDword2PostCall[i]), "--> Found char:", char, "--> Index in flag:", index)
    flag[index] = char

# Print flag
flagStr = ""
flagStr = flagStr.join(flag)
print("\nFlag is:", flagStr)

# --> FCSC{665cfa3e0277a889258cc9f6e24c88fc9db654178558de101b8a19af8fb00575}
