import { useContext } from "react";

import { Redirect } from "react-router-dom";

import { RoomsContext, SimpleForm } from "../components";
import { usePostRoom } from "../hooks";
import SimplePage from "./SimplePage";

export default function RoomsPage() {
  const { rooms } = useContext(RoomsContext);
  const createRoom = usePostRoom();

  const onFinish = (room) => {
    createRoom.mutate(room);
  };

  // If there are any rooms then redirect to the most recently active one
  if (rooms?.length) return <Redirect to={`/rooms/${rooms[0].id}`} />;

  return (
    <SimplePage title="Looks like you're the first one here. Get started by creating a room.">
      <SimpleForm
        buttonText="Create Room"
        errorMessage="A room with that name already exists"
        hasError={createRoom.isError}
        isLoading={createRoom.isLoading}
        name="createRoom"
        onFinish={onFinish}
        inputName="id"
        inputPlaceholder="Room name"
        inputValidationMessage="Please input a name for the room"
      />
    </SimplePage>
  );
}
