import { Layout } from "antd";
import { Messages, MessageEditor, Rooms } from "./components";

const { Header, Content, Footer, Sider } = Layout;

function ChatPage() {
  return (
    <Layout>
      <Sider theme="light" breakpoint="md" collapsedWidth="0">
        <Rooms />
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
            padding: "0 40px",
            height: "calc(100vh - 96px - 64px)",
            overflowY: "scroll",
            // Fancy css trick to keep the scroll pinned to the bottom. Neat!
            display: "flex",
            flexDirection: "column-reverse",
          }}
        >
          <Messages></Messages>
        </Content>
        <Footer
          style={{
            background: "#fff",
            paddingBottom: "40px",
          }}
        >
          <MessageEditor></MessageEditor>
        </Footer>
      </Layout>
    </Layout>
  );
}

export default ChatPage;
