
namespace BOXServer
{
    class BOXHEAD
    {
        public static void Main(string[] args)
        {
            SocketHandle socket = new SocketHandle();
            DBHandle db = new DBHandle();

            db.InitDB();
            socket.InitSocket();
        }
    }
}