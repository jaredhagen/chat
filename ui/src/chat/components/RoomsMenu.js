import { Button, Layout, Menu, Spin } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import { createContext, useContext, useState, useEffect } from "react";
import { Link, useHistory, useParams } from "react-router-dom";

import { useGetRooms } from "../hooks";

const RoomsMenuContext = createContext();

function RoomsMenuProvider({ children }) {
  const [collapsed, setCollapsed] = useState(false);
  const [selectedRoom, setSelectedRoom] = useState(false);
  return (
    <RoomsMenuContext.Provider
      value={{
        collapsed,
        setCollapsed,
        selectedRoom,
        setSelectedRoom,
      }}
    >
      {children}
    </RoomsMenuContext.Provider>
  );
}

function RoomsMenu() {
  const { collapsed, setCollapsed, selectedRoom, setSelectedRoom } = useContext(
    RoomsMenuContext
  );
  const urlParams = useParams();
  const history = useHistory();
  const { isLoading, error, data } = useGetRooms();

  useEffect(() => {
    // This is a bit of a mess.  If I had more time I'd figure out a better solution
    if (!isLoading && !selectedRoom && data.rooms.length) {
      let roomToSelect;
      // Set the selected room to the one in the url if we can find it
      if (urlParams.roomId) {
        roomToSelect = data.rooms.find((room) => room.id == urlParams.roomId);
      }
      // Otherwise select the most recently active room
      if (!roomToSelect) {
        roomToSelect = data.rooms[0];
        history.replace(`/rooms/${roomToSelect.id}`);
      }
      setSelectedRoom(roomToSelect);
    }
  });

  if (error) return <div>Womp!</div>;

  return (
    <Layout.Sider
      theme="light"
      breakpoint="md"
      collapsed={collapsed}
      collapsedWidth="0"
      onCollapse={(collapsed) => {
        setCollapsed(collapsed);
      }}
      trigger={null}
    >
      <div
        style={{
          width: "100%",
          padding: "15px 10px 10px 10px",
        }}
      >
        <Button block type="primary" icon={<PlusOutlined />}>
          Add A Room
        </Button>
      </div>
      {isLoading || !selectedRoom ? (
        <></>
      ) : (
        <Menu
          mode="inline"
          style={{
            height: "calc(100vh - 57px)",
            overflowX: "hidden",
            overflowY: "scroll",
          }}
          defaultSelectedKeys={[selectedRoom.id]}
        >
          {data.rooms.map((room) => (
            <Menu.Item
              key={room.id}
              onClick={() => {
                setSelectedRoom(room);
              }}
            >
              <Link to={`/rooms/${room.id}`}>{room.name}</Link>
            </Menu.Item>
          ))}
        </Menu>
      )}
    </Layout.Sider>
  );
}

export { RoomsMenu, RoomsMenuContext, RoomsMenuProvider };
