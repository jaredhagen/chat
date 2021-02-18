import { Layout } from "antd";
import {
  Messages,
  MessageEditor,
  RoomHeader,
  RoomsMenu,
  RoomsMenuProvider,
} from "./components";

export default function ChatPage() {
  return (
    <RoomsMenuProvider>
      <Layout>
        <RoomsMenu />
        <Layout>
          <RoomHeader />
          <Messages></Messages>
          <MessageEditor></MessageEditor>
        </Layout>
      </Layout>
    </RoomsMenuProvider>
  );
}
