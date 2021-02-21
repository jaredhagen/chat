import { Button, Layout, Menu } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import { createContext, useContext, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { AddRoomModalContext } from "./AddRoomModal";
import { RoomsContext } from "./RoomsProvider";

const RoomsMenuContext = createContext();

function RoomsMenuProvider({ children }) {
  const [collapsed, setCollapsed] = useState(false);
  return (
    <RoomsMenuContext.Provider
      value={{
        collapsed,
        setCollapsed,
      }}
    >
      {children}
    </RoomsMenuContext.Provider>
  );
}

function RoomsMenu() {
  const { collapsed, setCollapsed } = useContext(RoomsMenuContext);
  const { showModal } = useContext(AddRoomModalContext);
  const { rooms } = useContext(RoomsContext);
  const urlParams = useParams();

  return (
    <Layout.Sider
      theme="light"
      breakpoint="md"
      collapsed={collapsed}
      collapsedWidth="0"
      onCollapse={(collapse) => {
        setCollapsed(collapse);
      }}
      trigger={null}
    >
      <div
        style={{
          width: "100%",
          padding: "15px 10px 10px 10px",
        }}
      >
        <Button
          block
          type="primary"
          icon={<PlusOutlined />}
          onClick={showModal}
        >
          Add A Room
        </Button>
      </div>

      <Menu
        mode="inline"
        style={{
          height: "calc(100vh - 57px)",
          overflowX: "hidden",
          overflowY: "scroll",
        }}
        defaultSelectedKeys={[urlParams.roomId]}
      >
        {rooms?.map((room) => (
          <Menu.Item key={room.id}>
            <Link to={`/rooms/${room.id}`}>{room.name}</Link>
          </Menu.Item>
        ))}
      </Menu>
    </Layout.Sider>
  );
}

export { RoomsMenu, RoomsMenuContext, RoomsMenuProvider };
