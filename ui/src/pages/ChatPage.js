import { useContext } from "react";

import { Layout } from "antd";
import { Redirect, Route, Switch, useRouteMatch } from "react-router-dom";

import {
  AddRoomModalProvider,
  Messages,
  MessageEditor,
  RoomHeader,
  RoomsMenu,
  RoomsMenuProvider,
  RoomsContext,
  RoomsProvider,
} from "../components";
import { RoomsPage } from "../pages";

export default function ChatPage() {
  const { path } = useRouteMatch();

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
                  <Messages></Messages>
                  <MessageEditor></MessageEditor>
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
