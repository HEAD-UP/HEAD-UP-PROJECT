using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Text;
using Newtonsoft.Json.Linq;

namespace BOXServer
{
    class SocketHandle
    {
        SectionController sec1 = new SectionController();
        TcpListener server = null;
        TcpClient clientSocket = null;

        public void InitSocket() //소켓통신 accept 전용
        {
            Thread pthread = new Thread(sec1.StartController);
            pthread.IsBackground = true;
            pthread.Start();    //컨트롤러 실행

            server = new TcpListener(IPAddress.Any, 8990);
            clientSocket = default(TcpClient);
            server.Start();     //서버 실행

            try //accept
            {
                Console.WriteLine("Server Open.");
                while (true)
                {
                    clientSocket = server.AcceptTcpClient();
                    Receiver recv = new Receiver();
                    sec1.AddRecv(recv, clientSocket);
                }
            }

            catch (Exception ex) { }

            finally
            {
                clientSocket.Close();
                server.Stop();
            }
        }
    }

    class SectionController //각 구역별로 소켓 관리
    {
        List<Receiver> recvList = new List<Receiver>(); //리시버 관리용 리스트

        public void AddRecv(Receiver newrecv, TcpClient clientSocket) //리시버 등록
        {
            Console.WriteLine("New client.");
            newrecv.InitStream(clientSocket);
            recvList.Add(newrecv);
        }

        public void StartController() //컨트롤러 스레드 수행용
        {
            bool isDanger = false;
            int dangerPoint = 0, dangerCount = 0;

            try
            {
                while (true)
                {
                    for (int i = 0; i < recvList.Count; i++)
                    {
                        int point = recvList[i].RecvMsg();

                        if (point >= 0)
                        {
                            dangerPoint += point;
                            dangerCount++;
                        }
                    }

                    if (dangerPoint > 0 && dangerCount > 1)
                        isDanger = true;

                    for (int i = 0; i < recvList.Count; i++)
                    {
                        recvList[i].SendMsg(isDanger);
                    }

                    isDanger = false;
                    dangerPoint = 0;
                    dangerCount = 0;
                }
            }

            catch (Exception e)
            {
                Console.WriteLine(e);
                for (int i = 0; i < recvList.Count; i++)
                    recvList[i].Close();
            }
        }
    }

    class Receiver //클라이언트와 통신 담당
    {
        TcpClient client; //tcp정보
        NetworkStream NS;
        StreamReader SR;
        StreamWriter SW;

        public void InitStream(TcpClient tcpClient) //스트림 초기화
        {
            client = tcpClient;
            NS = client.GetStream();
            SR = new StreamReader(NS, Encoding.UTF8);
            SW = new StreamWriter(NS, Encoding.UTF8);
        }

        public int RecvMsg() //메시지 수신
        {
            JObject input = JObject.Parse(SR.ReadLine());

            Console.WriteLine("Camera_ID: {0}/ Value: {1}", (string)input["Camera_ID"], (string)input["Value"]);

            return (int)input["Value"];
        }

        public void SendMsg(bool isDanger) //메시지 전송
        {
            int output = 0;

            if (isDanger)
                output = 1;
            else
                output = 0;

            SW.WriteLine(output);
            SW.Flush();
        }

        public void Close() //소켓 해제
        {
            client.Close();
        }
    }
}
