package demo;



import ai.djl.Device;
import ai.djl.Model;
import ai.djl.inference.Predictor;
import ai.djl.ndarray.NDArray;
import ai.djl.ndarray.NDList;
import ai.djl.ndarray.NDManager;
import ai.djl.translate.NoBatchifyTranslator;
import ai.djl.translate.TranslatorContext;
import java.nio.file.Paths;

//Java调用pytorch的模型
public class Dataset {

    public String demo() {
        Model model = Model.newInstance("test");
        try (NDManager manager = NDManager.newBaseManager()) {
            model.load(Paths.get("model/linara.pt"));
            System.out.println(model);
            // 模型输入数据的调整 官方学习数据处理DIJ文档：https://d2l-zh.djl.ai/chapter_preliminaries/ndarray.html
            Predictor<NDArray, float[]> objectObjectPredictor = model.newPredictor(new NoBatchifyTranslator<NDArray, float[]>() {
                //这里的input会有另外类型
                @Override
                public NDList processInput(TranslatorContext translatorContext, NDArray input) throws Exception {
//                    NDArray ndArray = manager.create(input).reshape(input.length, -1);
                    //ndArray作为输入
                    System.out.println(input);
                    return new NDList(input);
                }

                // 输出的数据处理
                @Override
                public float[] processOutput(TranslatorContext translatorContext, NDList ndList) throws Exception {
                    return ndList.get(0).toFloatArray();
                }
            });

            NDArray ndArray = manager.arange(1, 2);
            System.out.println(ndArray);

            //创建模型的输入数据 并转为 (size, 1)的矩阵
            NDArray x = manager.create(new float[]{0.1f,0.2f,0.3f,0.4f,0.5f,0.6f,0.7f,
                    0.8f,0.9f,0.7f,0.8f,0.9f,0.7f,0.8f,0.9f,0.7f,0.8f,0.9f,0.7f,0.8f,0.9f,0.7f,0.8f,0.9f}).reshape(-1, 1);

            //调用模型的预测单元
            float[] result = objectObjectPredictor.predict(x);

            System.out.println("----");
//            System.out.println(result);
            for(float re:result) {
                System.out.println(re);
            }
//            model.newPredictor()

        } catch (Exception e) {
            System.out.println("qunimade ");
            e.printStackTrace();
        }

        return "ceshi";
    }

    public static void main(String[] args) {
        new Dataset().demo();
    }

     /*
    tensor([[0.1293],
        [0.1765],
        [0.2385],
        [0.2207],
        [0.3336],
        [0.4856],
        [0.6479],
        [0.8130],
        [0.8256],
        [0.5187],
        [0.6829],
        [0.8407],
        [0.6640],
        [0.6493],
        [0.9789],
        [0.6372],
        [0.8218],
        [0.8539],
        [0.6275],
        [0.7040],
        [0.9112],
        [0.5226],
        [0.7886],
        [0.9916]])

Process finished with exit code 0

     */

    /**
     * Debug环境的时候 Evaluate Expression 不能正常的显示，需要idea编译器里面设置一下，
     * 帮助的图片在 model/IDEA Debug时Evaluate Expression不能显示NDArray变量的问题.png 图片中显示
     *
     * 官方的帮助文档在 https://docs.djl.ai/docs/development/development_guideline.html，
     * 注意他们使用的MxNet，所以我们的引擎地址要改成pytorch的
     *
     */

}
