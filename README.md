# eve-ui-reader-conversion
I am working to port the Vir Bot Tools from ELM to Python.  When looking at memory readers, it seemed that the node hierarchy tree was being generated from Compiled C# code running Cython under the Hood.  My goal is to instead of using the ELM tool to parse the data and submit it, it would do it through python peeling back layers.  This is separate from other bot software previously written.