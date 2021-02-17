import { Menu, Spin } from "antd";
import { Link, useHistory, useLocation } from "react-router-dom";
import { useGetRooms } from "../hooks";

export default function Rooms() {
  const location = useLocation();
  const history = useHistory();
  const { isLoading, error, data } = useGetRooms();

  if (isLoading) return <Spin size="large" />;

  if (error) return <div>Womp!</div>;

  const rooms = data.rooms;

  // Load the most recently active room when no room is selected
  if (location.pathname == "/" && rooms.length) {
    history.push(`/rooms/${rooms[0].id}`);
  }

  return (
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
        <Menu.Item key={room.id}>
          <Link to={`/rooms/${room.id}`}>{room.name}</Link>
        </Menu.Item>
      ))}
    </Menu>
  );
}
