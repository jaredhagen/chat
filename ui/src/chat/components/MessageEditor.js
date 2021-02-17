import { Row, Col, Form, Input, Button, Space } from "antd";
import { useParams } from "react-router-dom";

import { usePostMessage } from "../hooks";

export default function MessageEditor() {
  const { roomId } = useParams();
  const postMessage = usePostMessage(roomId);

  const [form] = Form.useForm();
  const onFinish = (message) => {
    form.resetFields();
    postMessage.mutate(message);
  };
  return (
    <Form layout="inline" form={form} name="message" onFinish={onFinish}>
      <Col span={24}>
        <Row align="center" gutter={16}>
          <Col flex="auto">
            <Form.Item style={{ width: "100%" }} name={"content"}>
              <Input maxLength={1000} placeholder="Say something..." />
            </Form.Item>
          </Col>
          <Space align="center">
            <Col flex="none">
              <Form.Item>
                <Button type="primary" htmlType="submit">
                  Send Message
                </Button>
              </Form.Item>
            </Col>
          </Space>
        </Row>
      </Col>
    </Form>
  );
}
