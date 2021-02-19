import { Button, Col, Form, Input, Row, Spin, Typography } from "antd";
import { Redirect } from "react-router-dom";
import { useGetRooms, usePostRoom } from "./hooks";

export default function RoomsPage() {
  const { isLoading, error, data } = useGetRooms();
  const createRoom = usePostRoom();

  const onFinish = (room) => {
    createRoom.mutate(room);
  };

  if (isLoading) return <Spin />;

  if (error) return <div>Womp!</div>;

  if (data?.rooms?.length) {
    const mostRecentlyActiveRoomId = data.rooms[0];
    return <Redirect to={`/rooms/${mostRecentlyActiveRoomId.id}`} />;
  }

  return (
    <Row
      align="middle"
      style={{
        height: "100vh",
      }}
    >
      <Col span={24}>
        <Row justify="center">
          <Col>
            <Typography.Title level={2}>
              Looks like you're the first one here. Get started by creating a
              room.
            </Typography.Title>
          </Col>
        </Row>
        <Row justify="center">
          <Col span={8}>
            <Form
              name="createRoom"
              initialValues={{
                remember: true,
              }}
              onFinish={onFinish}
            >
              <Form.Item
                name="id"
                hasFeedback={createRoom.isLoading || createRoom.isError}
                validateStatus={
                  createRoom.isLoading
                    ? "validating"
                    : createRoom.isError
                    ? "error"
                    : ""
                }
                rules={[
                  {
                    required: true,
                    message: "Please input a name for the room",
                  },
                ]}
              >
                <Input placeholder="Room name" />
              </Form.Item>
              <Form.Item>
                <Button block type="primary" htmlType="submit">
                  Create room
                </Button>
              </Form.Item>
            </Form>
          </Col>
        </Row>
      </Col>
    </Row>
  );
}
