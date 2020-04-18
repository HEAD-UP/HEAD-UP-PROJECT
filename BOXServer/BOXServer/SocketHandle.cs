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
        TcpListener server = null;
        TcpClient clientSocket = null;
        public List<TcpClient> clientList = new List<TcpClient>();

        public void InitSocket()
        {
            server = new TcpListener(IPAddress.Any, 6974);
            clientSocket = default(TcpClient);
            server.Start();

            try
            {
                Console.WriteLine("Server Open.");
                while (true)
                {
                    clientSocket = server.AcceptTcpClient();
                    Receiver recv = new Receiver();
                    recv.startClient(clientSocket);
                }
            }

            catch (Exception ex) { }

            finally
            {
                foreach (TcpClient clnt in clientList)
                {
                    try
                    {
                        clientList.Remove(clnt);
                        clnt.Close();
                    }
                    catch (Exception e) { }
                }

                clientSocket.Close();
                server.Stop();
            }
        }
    }

    class Receiver
    {
        NetworkStream NS = null;
        StreamReader SR = null;
        StreamWriter SW = null;
        TcpClient client;

        public void startClient(TcpClient clientSocket)
        {
            client = clientSocket;
            Thread pthread = new Thread(process);
            pthread.IsBackground = true;
            pthread.Start();
        }

        public void process()
        {
            NS = client.GetStream();
            SR = new StreamReader(NS, Encoding.UTF8);
            SW = new StreamWriter(NS, Encoding.UTF8);
            string GetMessage = string.Empty;

            Console.WriteLine("New Client.");

            try
            {
                while(true)
                {
                    GetMessage = SR.ReadLine();
                    RecvMsg(GetMessage);
                }
            }
            catch (Exception e) { Console.WriteLine(e); close(); }
        }

        public void close()
        {
            try
            {
                SW.Close();
                SR.Close();
                client.Close();
                NS.Close();
                Console.WriteLine("Server Close.");
            }
            catch (Exception e) { }
        }

        private void RecvMsg(string msg)
        {
            JObject input = JObject.Parse(msg);

            Console.WriteLine("Camera_ID: {0}/ Value: {1}", (string)input["Camera_ID"], (string)input["Value"]);
        }

        public void SendMsg()
        {
            SW.Flush();
        }
    }
}
