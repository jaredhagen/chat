import { Button, Col, Layout, Menu, Row, Spin, Typography } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import { DateTime } from "luxon";
import { createContext, useContext, useState, useEffect } from "react";
import { Link, Redirect, useHistory, useParams } from "react-router-dom";

import { AddRoomModalContext } from "../components";
import { useGetRooms, usePostRoom } from "../hooks";

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
  const { showModal } = useContext(AddRoomModalContext);
  const urlParams = useParams();
  const { isLoading, error, data } = useGetRooms();

  useEffect(() => {
    // This is a bit of a mess.  If I had more time I'd figure out a better solution
    if (!isLoading && !selectedRoom && data.rooms.length) {
      let roomToSelect;
      // Set the selected room to the one in the url if we can find it
      if (urlParams.roomId) {
        roomToSelect = data.rooms.find((room) => room.id == urlParams.roomId);
        if (!roomToSelect) {
        }
      }
      setSelectedRoom(roomToSelect);
    }
  });

  if (isLoading) return <Spin />;

  if (error) return <div>Womp!</div>;

  if (data?.rooms?.length == 0) {
    return <Redirect to={`/`} />;
  }

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
        <Button
          block
          type="primary"
          icon={<PlusOutlined />}
          onClick={showModal}
        >
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
          {data?.rooms?.map((room) => (
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
