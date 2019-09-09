package main

import (
	"crypto/rc4"
	"encoding/base64"
	"fmt"
	"io"
	"io/ioutil"
	"net"
	"os"
	"strings"
	"time"
)

const RECV_BUF_LEN = 1024

const wmax = 233

var node67 = &Tree{v: 29, w: 22, is_chosen: false, father: node45}
var node77 = &Tree{v: 84, w: 28, is_chosen: false, father: node58}
var node3 = &Tree{v: 15, w: 10, is_chosen: false, father: node0}
var node95 = &Tree{v: 58, w: 34, is_chosen: false, father: node90}
var node74 = &Tree{v: 24, w: 41, is_chosen: false, father: node56}
var node70 = &Tree{v: 73, w: 41, is_chosen: false, father: node51}
var node94 = &Tree{v: 70, w: 33, is_chosen: false, father: node89}
var node62 = &Tree{v: 19, w: 13, is_chosen: false, father: node39}
var node89 = &Tree{v: 86, w: 12, is_chosen: false, father: node75}
var node72 = &Tree{v: 100, w: 36, is_chosen: false, father: node55}
var node44 = &Tree{v: 84, w: 17, is_chosen: false, father: node23}
var node97 = &Tree{v: 82, w: 1, is_chosen: false, father: node91}
var node15 = &Tree{v: 54, w: 41, is_chosen: false, father: node5}
var node82 = &Tree{v: 22, w: 10, is_chosen: false, father: node69}
var node60 = &Tree{v: 40, w: 36, is_chosen: false, father: node38}
var node84 = &Tree{v: 99, w: 5, is_chosen: false, father: node70}
var node4 = &Tree{v: 2, w: 18, is_chosen: false, father: node0}
var node61 = &Tree{v: 35, w: 19, is_chosen: false, father: node38}
var node0 = &Tree{v: 82, w: 6, is_chosen: false, father: nil}
var node26 = &Tree{v: 92, w: 15, is_chosen: false, father: node10}
var node41 = &Tree{v: 46, w: 45, is_chosen: false, father: node21}
var node46 = &Tree{v: 11, w: 34, is_chosen: false, father: node27}
var node22 = &Tree{v: 25, w: 1, is_chosen: false, father: node8}
var node93 = &Tree{v: 11, w: 135, is_chosen: false, father: node81}
var node99 = &Tree{v: 480, w: 55, is_chosen: false, father: node93}
var node86 = &Tree{v: 86, w: 3, is_chosen: false, father: node73}
var node13 = &Tree{v: 99, w: 17, is_chosen: false, father: node4}
var node42 = &Tree{v: 71, w: 13, is_chosen: false, father: node22}
var node49 = &Tree{v: 36, w: 11, is_chosen: false, father: node28}
var node11 = &Tree{v: 46, w: 8, is_chosen: false, father: node3}
var node39 = &Tree{v: 14, w: 27, is_chosen: false, father: node21}
var node27 = &Tree{v: 82, w: 32, is_chosen: false, father: node11}
var node53 = &Tree{v: 7, w: 17, is_chosen: false, father: node32}
var node81 = &Tree{v: 49, w: 37, is_chosen: false, father: node66}
var node73 = &Tree{v: 86, w: 39, is_chosen: false, father: node55}
var node50 = &Tree{v: 79, w: 32, is_chosen: false, father: node31}
var node18 = &Tree{v: 56, w: 33, is_chosen: false, father: node7}
var node66 = &Tree{v: 8, w: 43, is_chosen: false, father: node44}
var node1 = &Tree{v: 46, w: 31, is_chosen: false, father: node0}
var node57 = &Tree{v: 4, w: 26, is_chosen: false, father: node35}
var node6 = &Tree{v: 54, w: 22, is_chosen: false, father: node1}
var node98 = &Tree{v: 398, w: 68, is_chosen: false, father: node93}
var node45 = &Tree{v: 26, w: 4, is_chosen: false, father: node26}
var node34 = &Tree{v: 15, w: 29, is_chosen: false, father: node16}
var node17 = &Tree{v: 30, w: 34, is_chosen: false, father: node7}
var node78 = &Tree{v: 10, w: 20, is_chosen: false, father: node58}
var node58 = &Tree{v: 16, w: 25, is_chosen: false, father: node35}
var node8 = &Tree{v: 1, w: 36, is_chosen: false, father: node3}
var node38 = &Tree{v: 13, w: 20, is_chosen: false, father: node20}
var node24 = &Tree{v: 4, w: 2, is_chosen: false, father: node10}
var node36 = &Tree{v: 100, w: 5, is_chosen: false, father: node17}
var node83 = &Tree{v: 93, w: 46, is_chosen: false, father: node69}
var node79 = &Tree{v: 99, w: 37, is_chosen: false, father: node60}
var node28 = &Tree{v: 54, w: 8, is_chosen: false, father: node11}
var node12 = &Tree{v: 47, w: 34, is_chosen: false, father: node3}
var node91 = &Tree{v: 59, w: 15, is_chosen: false, father: node76}
var node14 = &Tree{v: 75, w: 50, is_chosen: false, father: node4}
var node65 = &Tree{v: 31, w: 43, is_chosen: false, father: node43}
var node88 = &Tree{v: 91, w: 11, is_chosen: false, father: node75}
var node51 = &Tree{v: 45, w: 50, is_chosen: false, father: node31}
var node59 = &Tree{v: 35, w: 3, is_chosen: false, father: node35}
var node32 = &Tree{v: 49, w: 8, is_chosen: false, father: node16}
var node7 = &Tree{v: 14, w: 16, is_chosen: false, father: node1}
var node35 = &Tree{v: 61, w: 50, is_chosen: false, father: node16}
var node54 = &Tree{v: 54, w: 28, is_chosen: false, father: node32}
var node43 = &Tree{v: 59, w: 39, is_chosen: false, father: node22}
var node56 = &Tree{v: 99, w: 6, is_chosen: false, father: node35}
var node75 = &Tree{v: 24, w: 27, is_chosen: false, father: node56}
var node23 = &Tree{v: 82, w: 48, is_chosen: false, father: node8}
var node30 = &Tree{v: 98, w: 44, is_chosen: false, father: node15}
var node37 = &Tree{v: 65, w: 22, is_chosen: false, father: node18}
var node52 = &Tree{v: 81, w: 21, is_chosen: false, father: node32}
var node92 = &Tree{v: 19, w: 42, is_chosen: false, father: node77}
var node25 = &Tree{v: 16, w: 3, is_chosen: false, father: node10}
var node68 = &Tree{v: 20, w: 21, is_chosen: false, father: node47}
var node31 = &Tree{v: 71, w: 2, is_chosen: false, father: node16}
var node10 = &Tree{v: 86, w: 6, is_chosen: false, father: node3}
var node85 = &Tree{v: 45, w: 44, is_chosen: false, father: node71}
var node76 = &Tree{v: 19, w: 16, is_chosen: false, father: node56}
var node9 = &Tree{v: 43, w: 17, is_chosen: false, father: node3}
var node64 = &Tree{v: 18, w: 4, is_chosen: false, father: node41}
var node80 = &Tree{v: 97, w: 8, is_chosen: false, father: node63}
var node48 = &Tree{v: 74, w: 40, is_chosen: false, father: node27}
var node90 = &Tree{v: 66, w: 25, is_chosen: false, father: node75}
var node63 = &Tree{v: 85, w: 34, is_chosen: false, father: node40}
var node20 = &Tree{v: 44, w: 23, is_chosen: false, father: node7}
var node21 = &Tree{v: 26, w: 43, is_chosen: false, father: node8}
var node5 = &Tree{v: 51, w: 22, is_chosen: false, father: node1}
var node69 = &Tree{v: 12, w: 7, is_chosen: false, father: node48}
var node19 = &Tree{v: 79, w: 11, is_chosen: false, father: node7}
var node2 = &Tree{v: 53, w: 40, is_chosen: false, father: node0}
var node55 = &Tree{v: 59, w: 28, is_chosen: false, father: node32}
var node87 = &Tree{v: 64, w: 24, is_chosen: false, father: node74}
var node71 = &Tree{v: 9, w: 34, is_chosen: false, father: node53}
var node33 = &Tree{v: 19, w: 29, is_chosen: false, father: node16}
var node96 = &Tree{v: 37, w: 14, is_chosen: false, father: node91}
var node29 = &Tree{v: 71, w: 48, is_chosen: false, father: node11}
var node16 = &Tree{v: 6, w: 2, is_chosen: false, father: node5}
var node40 = &Tree{v: 72, w: 28, is_chosen: false, father: node21}
var node47 = &Tree{v: 19, w: 17, is_chosen: false, father: node27}

var nodes []*Tree = []*Tree{node0, node1, node2, node3, node4, node5, node6, node7, node8, node9, node10, node11, node12, node13, node14, node15, node16, node17, node18, node19, node20, node21, node22, node23, node24, node25, node26, node27, node28, node29, node30, node31, node32, node33, node34, node35, node36, node37, node38, node39, node40, node41, node42, node43, node44, node45, node46, node47, node48, node49, node50, node51, node52, node53, node54, node55, node56, node57, node58, node59, node60, node61, node62, node63, node64, node65, node66, node67, node68, node69, node70, node71, node72, node73, node74, node75, node76, node77, node78, node79, node80, node81, node82, node83, node84, node85, node86, node87, node88, node89, node90, node91, node92, node93, node94, node95, node96, node97, node98, node99}

type Tree struct {
	v         int
	w         int
	is_chosen bool
	father    *Tree
}

func main() {
	list := os.Args
	if len(list) == 1 {
		run_server()
	} else {
		var s string
		fmt.Scanf("%s", &s)
		x := client(list[1], s)
		if len(x) > 0 {
			fmt.Println(x)
		}
	}
}

func run_server() {
	listener, err := net.Listen("tcp", "0.0.0.0:30754")
	if err != nil {
		panic("error listening:" + err.Error())
	}
	//fmt.Println("Starting the server")

	flag1, err := ioutil.ReadFile("flag1.txt")
	if err != nil {
		//fmt.Println("flag1 reading error", err)
		return
	}

	flag2, err := ioutil.ReadFile("flag2.txt")
	if err != nil {
		//fmt.Println("flag2 reading error", err)
		return
	}

	for {
		conn, err := listener.Accept()
		if err != nil {
			panic("Error accept:" + err.Error())
		}
		conn.SetReadDeadline(time.Now().Add(time.Duration(10) * time.Second))
		fmt.Println("Accept:", conn.RemoteAddr())
		go my_server(conn, flag1, flag2)
	}
}

func client(addr string, s string) string {
	conn, err := net.Dial("tcp", addr+":30754")
	if err != nil {
		panic(err.Error())
	}
	defer conn.Close()

	buf := make([]byte, RECV_BUF_LEN)

	msg := s
	n, err := conn.Write([]byte(msg))
	if err != nil {
		//println("Write Buffer Error:", err.Error())
		return ""
	}

	n, err = conn.Read(buf)
	if err != nil {
		//println("Read Buffer Error:", err.Error())
		return ""
	}
	return string(buf[0:n])
}

var chars string = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c"

func check(input string) int {
	//fmt.Printf("start check")
	tot_v := 0
	tot_w := 0
	tot_v += tot_w
	for _, node := range nodes {
		node.is_chosen = false
	}
	s := dec(input)
	//fmt.Printf("checking %s\n", s)
	var lst_idx int = -1
	for index, char := range s {
		var idx int = strings.IndexRune(chars, char)
		//fmt.Printf("%d %d %c \n", index, idx, char)
		if idx == -1 || idx >= len(nodes) || (index != 0 && idx <= lst_idx) {
			//fmt.Printf("error at %c %d\n", char, index)
			return 0
		}
		lst_idx = idx
		cur_node := nodes[idx]
		//fmt.Printf("choose %d\n", idx)
		//if cur_node.father != nil {
		//	fmt.Printf("fa v: %d w: %d\n", cur_node.father.v, cur_node.father.w)
		//}
		if cur_node.father == nil || cur_node.father.is_chosen { // || true {
			tot_v += cur_node.v
			tot_w += cur_node.w
			cur_node.is_chosen = true
			//fmt.Printf("%d %d\n", tot_v, tot_w)
		} else {
			//fmt.Printf("tree invalid at %c %d\n", char, index)
			return 0
		}
	}
	//fmt.Printf("result of %s: %d %d\n", s, tot_v, tot_w)
	if tot_v >= 1050 && tot_w <= wmax {
		//fmt.Printf("ok %s flag2\n", s)
		return 2
	}
	if tot_v >= 560 && tot_w <= wmax {
		//fmt.Printf("ok %s flag1\n", s)
		return 1
	}
	fmt.Printf("'%s' failed\n", s)
	return 0
}

func dec(s string) string {
	key := []byte("This is not the key")
	enc_table := []byte{246, 204, 74, 73, 70, 135, 11, 116, 12, 81, 10, 7, 145, 228, 200, 227, 1, 11, 242, 127, 11, 32, 87, 123, 167, 168, 154, 242, 117, 152, 190, 97, 166, 7, 213, 104, 237, 151, 0, 153, 112, 147, 14, 20, 252, 147, 23, 112, 188, 157, 126, 120, 223, 236, 199, 217, 44, 229, 36, 107, 109, 169, 190, 86}
	for i := 0; i < 1024; i++ {
		rc4obj1, _ := rc4.NewCipher(key)
		rc4obj1.XORKeyStream(key, key)
	}
	rc4obj1, _ := rc4.NewCipher(key)
	rc4obj1.XORKeyStream(enc_table, enc_table)

	enc := base64.NewEncoding(string(enc_table))
	msg, err := enc.DecodeString(s)
	ret := ""
	if err != nil {
		//println("Base64 decode error:", err.Error())
	} else {
		ret = string(msg)
	}
	return ret
}

func my_server(conn net.Conn, flag1 []byte, flag2 []byte) {
	buf := make([]byte, RECV_BUF_LEN)
	defer conn.Close()
	//fmt.Println("Accepted the Connection :", conn.RemoteAddr() )
	for {
		n, err := conn.Read(buf)
		switch err {
		case nil:
			s := string(buf[0:n])
			check_result := check(s)
			switch {
			case check_result == 1:
				conn.Write(flag1)
				return
			case check_result == 2:
				conn.Write([]byte(string(flag1) + string(flag2)))
				return
			default:
				conn.Write([]byte("n"))
				return
			}

		case io.EOF:
			//fmt.Printf("End of data: %s \n", err)
			return
		default:
			//fmt.Printf("Error Reading data : %s \n", err)
			return
		}
	}
}
