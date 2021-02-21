import { Layout, List, Space, Typography } from "antd";
import { DateTime } from "luxon";
import { useParams } from "react-router-dom";

import { useGetMessages } from "../hooks";

export default function Messages() {
  const { roomId } = useParams();
  const { isLoading, error, data } = useGetMessages(roomId);

  if (error) return <div>Womp!</div>;

  return (
    <Layout.Content
      style={{
        background: "#fff",
        padding: "0 40px",
        height: "calc(100vh - 96px - 64px)",
        overflowY: "scroll",
        // Fancy css trick to keep the scroll pinned to the bottom. Neat!
        display: "flex",
        flexDirection: "column-reverse",
      }}
    >
      <List
        size="small"
        loading={isLoading}
        locale={{
          emptyText: (
            <h3 style={{ marginTop: "-40vh" }}>
              Be the first to say something!
            </h3>
          ),
        }}
        itemLayout="horizontal"
        dataSource={data?.messages.slice().reverse()}
        renderItem={(message) => (
          <List.Item>
            <List.Item.Meta
              title={
                <Space direction="horizontal">
                  <Typography.Text>{message.author}</Typography.Text>
                  <Typography.Text style={{ fontSize: ".7rem", color: "#bbb" }}>
                    {/* Having to subtract a second to get the relative time to display nicely for new messages */}
                    {DateTime.fromMillis(message.createdAt - 1).toRelative()}
                  </Typography.Text>
                </Space>
              }
              description={message.content}
            />
          </List.Item>
        )}
      />
    </Layout.Content>
  );
}
