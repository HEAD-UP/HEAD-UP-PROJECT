using System;
using System.Data;
using System.Data.SQLite;

namespace BOXServer
{
    class DBHandle
    {
        private SQLiteConnection conn;
        private const string DbFile = "Data.db";
        private string ConnectionString = string.Format("Data Source={0};Version=3;", DbFile);

        public void InitDB()
        {
            try
            {
                if (!System.IO.File.Exists(DbFile))
                {
                    SQLiteConnection.CreateFile(DbFile);
                }

                // 테이블 생성
                conn = new SQLiteConnection(ConnectionString);
                conn.Open();

                string strsql = "CREATE TABLE IF NOT EXISTS Info (SectionID varchar(20), CameraID varchar(20))";

                SQLiteCommand cmd = new SQLiteCommand(strsql, conn);
                cmd.ExecuteNonQuery();
                conn.Close();
            }
            catch (Exception ex)
            {
                return;
            }
        }

        public void AddAccount(string ID, string PW)
        {
            conn.Open();

            string strsql = string.Format("select IFNULL(count(*), 0) from account where ='{0}'", ID);
            SQLiteCommand cmd = new SQLiteCommand(strsql, conn);

            Int64 idnum = (Int64)cmd.ExecuteScalar();

            if (idnum > 0)
            {

            }
            else
            {
                strsql = string.Format("insert into account values ('{0}', '{1}')", ID, PW);
                cmd = new SQLiteCommand(strsql, conn);

                cmd.ExecuteNonQuery();
            }
            conn.Close();

            DataSet ds = GetData();
        }

        public void UpdAccount(string ID, string PW)
        {
            conn.Open();

            string strsql = string.Format("update account set PW='{0}' where ID='{1}'", PW, ID);
            SQLiteCommand cmd = new SQLiteCommand(strsql, conn);

            cmd.ExecuteNonQuery();
            conn.Close();

            DataSet ds = GetData();
        }

        public void DelAccount()
        {
            conn.Open();

            string strsql = string.Format("delete from account where id=");
            SQLiteCommand cmd = new SQLiteCommand(strsql, conn);

            cmd.ExecuteNonQuery();
            conn.Close();

            DataSet ds = GetData();
        }

        private DataSet GetData()
        {
            conn.Open();

            SQLiteDataAdapter adapter = new SQLiteDataAdapter("SELECT * FROM Info", conn);
            DataSet ds = new DataSet();
            adapter.Fill(ds);

            conn.Close();

            return ds;
        }
    }
}
