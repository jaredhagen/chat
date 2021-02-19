import { Button, Col, Form, Input, Layout, Row, Space } from "antd";
import { useParams } from "react-router-dom";

import { usePostMessage } from "../hooks";

export default function MessageEditor() {
  const { roomId } = useParams();
  const postMessage = usePostMessage(roomId);

  const [form] = Form.useForm();
  const onFinish = (message) => {
    if (message.content) {
      form.resetFields();
      form.getFieldInstance("content").focus();
      postMessage.mutate(message);
    }
  };
  return (
    <Layout.Footer
      style={{
        background: "#fff",
        paddingBottom: "40px",
      }}
    >
      <Form layout="inline" form={form} name="message" onFinish={onFinish}>
        <Col span={24}>
          <Row align="center" gutter={16}>
            <Col flex="auto">
              <Form.Item style={{ width: "100%" }} name="content">
                <Input
                  autoComplete="off"
                  maxLength={1000}
                  placeholder="Say something..."
                />
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
    </Layout.Footer>
  );
}
