import { Layout, Menu, Spin } from "antd";
import Messages from "./Messages";
import { useRooms } from "./hooks";

const { Header, Content, Footer, Sider } = Layout;

function ChatPage() {
  const { isLoading, error, data } = useRooms();

  if (isLoading) return <Spin size="large" />;

  if (error) return <div>Womp!</div>;

  const rooms = data.rooms;

  return (
    <Layout>
      <Sider theme="light" breakpoint="md" collapsedWidth="0">
        <Menu
          mode="inline"
          style={{
            height: "100vh",
            overflowX: "hidden",
            overflowY: "scroll",
          }}
        >
          <Menu.Item>Add A Room</Menu.Item>
          {rooms.map((room) => (
            <Menu.Item>{room.name}</Menu.Item>
          ))}
        </Menu>
      </Sider>
      <Layout>
        <Header
          style={{
            background: "#fff",
          }}
        >
          Header
        </Header>
        <Content
          style={{
            background: "#fff",
          }}
        >
          <Messages></Messages>
        </Content>
        <Footer
          style={{
            background: "#fff",
          }}
        >
          Footer
        </Footer>
      </Layout>
    </Layout>
  );
}

export default ChatPage;
