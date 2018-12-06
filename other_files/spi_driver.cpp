struct mydevice_priv {
  struct spi_device *spi;
  struct spi_message spi_msg;
  struct spi_transfer spi_xfer;
  char data_tx[500];
  char data_rx[500];
};

static irqreturn_t mydevice_irq_handler(int irq, void *dev_id)
{
  struct mydevice_priv *priv = dev_id;
  struct spi_device *spi = priv->spi;

  /* execute the prepared spi-message asynchronously */
  spi_async(spi, spi_msg);
  /* note that you need to make sure that only one interrupt occurs,
   * as the same message can not be in flight multiple times...*/
}

static void mydevice_spi_msg_finished(void *context)
{
  struct mydevice_priv *priv = context;
  /* do whatever you want here */
}

static int mydevice_probe(struct spi_device *spi)
{
  int err;
  struct mydevice_priv *priv;

  /* allocate private structure */
  priv = devm_zalloc(sizeof(*priv),GPF_KERNEL);
  if (!priv)
    return -ENOMEM;

  /* set up things */
  priv->spi = dev;

  /* initialize spi message */
  spi_message_init(&priv->spi_msg);
  spi_message_add_tail(&priv->spi_xfer, &priv->spi_msg);

  /* only transfer data to device */
  priv->spi_xfer.len = sizeof(data);
  priv->spi_xfer.tx = data_tx;
  priv->spi_xfer.rx = data_rx;

  /* what to call asynchronously when the transfer is done */
  priv->spi_msg.complete = mydevice_spi_msg_finished;
  priv->spi_msg.context = priv;

  /* register irq handler */  
  err = devm_request_irq(spi->irq, NULL, mydevice_irq_handler, 0, DEVICE_NAME, priv);
  if (!ret)
    return err;

  /* other preparation stuff */
  ...

  /* return ok */
  return 0;
}

static const struct of_device_id mydevice_of_match[] = {
        {
                /* compatiblity string - typically <vendor>,<chip> */
                .compatible     = "mydevice-name-in-devicetree",
        },
        { }
};
MODULE_DEVICE_TABLE(of, mydevice_of_match);

static struct spi_driver mydevice_driver = {
        .driver = {
                .name = DEVICE_NAME,
                .owner = THIS_MODULE,
                .of_match_table = mydevice_of_match,
        },
        .id_table = mydevice_id_table,
        .probe = mydevice_probe,
};
module_spi_driver(mydevice_driver);

MODULE_AUTHOR("whatever");
MODULE_DESCRIPTION("whatever");
MODULE_LICENSE("GPL");