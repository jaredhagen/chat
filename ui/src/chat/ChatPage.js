import { Layout } from "antd";
import {
  Messages,
  MessageEditor,
  RoomHeader,
  RoomsMenu,
  RoomsMenuProvider,
} from "./components";
import { AddRoomModalProvider } from "./components/AddRoomModal";

export default function ChatPage() {
  return (
    <RoomsMenuProvider>
      <AddRoomModalProvider>
        <Layout>
          <RoomsMenu />
          <Layout>
            <RoomHeader />
            <Messages></Messages>
            <MessageEditor></MessageEditor>
          </Layout>
        </Layout>
      </AddRoomModalProvider>
    </RoomsMenuProvider>
  );
}
