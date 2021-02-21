import { Layout } from "antd";
import { Route, Switch } from "react-router-dom";

import {
  AddRoomModalProvider,
  Messages,
  MessageEditor,
  RoomHeader,
  RoomsMenu,
  RoomsMenuProvider,
  RoomsProvider,
} from "../components";
import RoomsPage from "./RoomsPage";

export default function ChatPage() {
  return (
    <RoomsProvider>
      <RoomsMenuProvider>
        <Switch>
          <Route path="/rooms/:roomId">
            <AddRoomModalProvider>
              <Layout>
                <RoomsMenu />
                <Layout>
                  <RoomHeader />
                  <Messages />
                  <MessageEditor />
                </Layout>
              </Layout>
            </AddRoomModalProvider>
          </Route>
          <Route path={["/rooms", "/"]}>
            <RoomsPage />
          </Route>
        </Switch>
      </RoomsMenuProvider>
    </RoomsProvider>
  );
}
