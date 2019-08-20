# Contains the source file definitions in src/compiler.gn
#
# This is a direct mapping of ALL values unless otherwise specified. All
# declarations are in the same ordering as the original .gn file

set(angle_translator_sources
    include/EGL/egl.h
    include/EGL/eglext.h
    include/EGL/eglplatform.h
    include/GLES2/gl2.h
    include/GLES2/gl2ext.h
    include/GLES2/gl2platform.h
    include/GLES3/gl3.h
    include/GLES3/gl3platform.h
    include/GLES3/gl31.h
    include/GLES3/gl32.h
    include/GLSLANG/ShaderLang.h
    include/GLSLANG/ShaderVars.h
    include/KHR/khrplatform.h
    include/angle_gl.h
    src/compiler/translator/BaseTypes.h
    src/compiler/translator/BuiltInFunctionEmulator.cpp
    src/compiler/translator/BuiltInFunctionEmulator.h
    src/compiler/translator/CallDAG.cpp
    src/compiler/translator/CallDAG.h
    src/compiler/translator/CodeGen.cpp
    src/compiler/translator/CollectVariables.cpp
    src/compiler/translator/CollectVariables.h
    src/compiler/translator/Common.h
    src/compiler/translator/Compiler.cpp
    src/compiler/translator/Compiler.h
    src/compiler/translator/ConstantUnion.cpp
    src/compiler/translator/ConstantUnion.h
    src/compiler/translator/Declarator.cpp
    src/compiler/translator/Declarator.h
    src/compiler/translator/Diagnostics.cpp
    src/compiler/translator/Diagnostics.h
    src/compiler/translator/DirectiveHandler.cpp
    src/compiler/translator/DirectiveHandler.h
    src/compiler/translator/ExtensionBehavior.cpp
    src/compiler/translator/ExtensionBehavior.h
    src/compiler/translator/FlagStd140Structs.cpp
    src/compiler/translator/FlagStd140Structs.h
    src/compiler/translator/FunctionLookup.cpp
    src/compiler/translator/FunctionLookup.h
    src/compiler/translator/HashNames.cpp
    src/compiler/translator/HashNames.h
    src/compiler/translator/ImmutableString_autogen.cpp
    src/compiler/translator/ImmutableString.h
    src/compiler/translator/ImmutableStringBuilder.cpp
    src/compiler/translator/ImmutableStringBuilder.h
    src/compiler/translator/InfoSink.cpp
    src/compiler/translator/InfoSink.h
    src/compiler/translator/Initialize.cpp
    src/compiler/translator/Initialize.h
    src/compiler/translator/InitializeDll.cpp
    src/compiler/translator/InitializeDll.h
    src/compiler/translator/InitializeGlobals.h
    src/compiler/translator/IntermNode.h
    src/compiler/translator/IntermNode.cpp
    src/compiler/translator/IsASTDepthBelowLimit.cpp
    src/compiler/translator/IsASTDepthBelowLimit.h
    src/compiler/translator/Operator.cpp
    src/compiler/translator/Operator.h
    src/compiler/translator/OutputTree.cpp
    src/compiler/translator/OutputTree.h
    src/compiler/translator/ParseContext.cpp
    src/compiler/translator/ParseContext.h
    src/compiler/translator/ParseContext_autogen.h
    src/compiler/translator/PoolAlloc.cpp
    src/compiler/translator/PoolAlloc.h
    src/compiler/translator/Pragma.h
    src/compiler/translator/QualifierTypes.h
    src/compiler/translator/QualifierTypes.cpp
    src/compiler/translator/Severity.h
    src/compiler/translator/ShaderLang.cpp
    src/compiler/translator/ShaderVars.cpp
    src/compiler/translator/StaticType.h
    src/compiler/translator/Symbol.cpp
    src/compiler/translator/Symbol.h
    src/compiler/translator/SymbolTable.cpp
    src/compiler/translator/SymbolTable.h
    src/compiler/translator/SymbolTable_autogen.cpp
    src/compiler/translator/SymbolTable_autogen.h
    src/compiler/translator/SymbolUniqueId.cpp
    src/compiler/translator/SymbolUniqueId.h
    src/compiler/translator/Types.cpp
    src/compiler/translator/Types.h
    src/compiler/translator/ValidateAST.cpp
    src/compiler/translator/ValidateAST.h
    src/compiler/translator/ValidateGlobalInitializer.cpp
    src/compiler/translator/ValidateGlobalInitializer.h
    src/compiler/translator/ValidateLimitations.cpp
    src/compiler/translator/ValidateLimitations.h
    src/compiler/translator/ValidateMaxParameters.h
    src/compiler/translator/ValidateMaxParameters.cpp
    src/compiler/translator/ValidateOutputs.cpp
    src/compiler/translator/ValidateOutputs.h
    src/compiler/translator/ValidateSwitch.cpp
    src/compiler/translator/ValidateSwitch.h
    src/compiler/translator/ValidateVaryingLocations.cpp
    src/compiler/translator/ValidateVaryingLocations.h
    src/compiler/translator/VariablePacker.cpp
    src/compiler/translator/VariablePacker.h
    src/compiler/translator/blocklayout.cpp
    src/compiler/translator/blocklayout.h
    src/compiler/translator/glslang.h
    src/compiler/translator/glslang_lex.cpp
    src/compiler/translator/glslang_tab.cpp
    src/compiler/translator/glslang_tab.h
    src/compiler/translator/length_limits.h
    src/compiler/translator/util.cpp
    src/compiler/translator/util.h
    src/compiler/translator/tree_ops/AddAndTrueToLoopCondition.cpp
    src/compiler/translator/tree_ops/AddAndTrueToLoopCondition.h
    src/compiler/translator/tree_ops/BreakVariableAliasingInInnerLoops.cpp
    src/compiler/translator/tree_ops/BreakVariableAliasingInInnerLoops.h
    src/compiler/translator/tree_ops/ClampFragDepth.cpp
    src/compiler/translator/tree_ops/ClampFragDepth.h
    src/compiler/translator/tree_ops/ClampPointSize.cpp
    src/compiler/translator/tree_ops/ClampPointSize.h
    src/compiler/translator/tree_ops/DeclareAndInitBuiltinsForInstancedMultiview.h
    src/compiler/translator/tree_ops/DeclareAndInitBuiltinsForInstancedMultiview.cpp
    src/compiler/translator/tree_ops/DeferGlobalInitializers.cpp
    src/compiler/translator/tree_ops/DeferGlobalInitializers.h
    src/compiler/translator/tree_ops/EmulateGLFragColorBroadcast.cpp
    src/compiler/translator/tree_ops/EmulateGLFragColorBroadcast.h
    src/compiler/translator/tree_ops/EmulateMultiDrawShaderBuiltins.cpp
    src/compiler/translator/tree_ops/EmulateMultiDrawShaderBuiltins.h
    src/compiler/translator/tree_ops/EmulatePrecision.cpp
    src/compiler/translator/tree_ops/EmulatePrecision.h
    src/compiler/translator/tree_ops/ExpandIntegerPowExpressions.cpp
    src/compiler/translator/tree_ops/ExpandIntegerPowExpressions.h
    src/compiler/translator/tree_ops/FoldExpressions.cpp
    src/compiler/translator/tree_ops/FoldExpressions.h
    src/compiler/translator/tree_ops/InitializeVariables.cpp
    src/compiler/translator/tree_ops/InitializeVariables.h
    src/compiler/translator/tree_ops/NameEmbeddedUniformStructs.cpp
    src/compiler/translator/tree_ops/NameEmbeddedUniformStructs.h
    src/compiler/translator/tree_ops/PruneEmptyCases.cpp
    src/compiler/translator/tree_ops/PruneEmptyCases.h
    src/compiler/translator/tree_ops/PruneNoOps.cpp
    src/compiler/translator/tree_ops/PruneNoOps.h
    src/compiler/translator/tree_ops/RecordConstantPrecision.cpp
    src/compiler/translator/tree_ops/RecordConstantPrecision.h
    src/compiler/translator/tree_ops/RegenerateStructNames.cpp
    src/compiler/translator/tree_ops/RegenerateStructNames.h
    src/compiler/translator/tree_ops/RemoveArrayLengthMethod.cpp
    src/compiler/translator/tree_ops/RemoveArrayLengthMethod.h
    src/compiler/translator/tree_ops/RemoveInvariantDeclaration.cpp
    src/compiler/translator/tree_ops/RemoveInvariantDeclaration.h
    src/compiler/translator/tree_ops/RemovePow.cpp
    src/compiler/translator/tree_ops/RemovePow.h
    src/compiler/translator/tree_ops/RemoveUnreferencedVariables.cpp
    src/compiler/translator/tree_ops/RemoveUnreferencedVariables.h
    src/compiler/translator/tree_ops/RewriteAtomicCounters.cpp
    src/compiler/translator/tree_ops/RewriteAtomicCounters.h
    src/compiler/translator/tree_ops/RewriteAtomicFunctionExpressions.cpp
    src/compiler/translator/tree_ops/RewriteAtomicFunctionExpressions.h
    src/compiler/translator/tree_ops/RewriteCubeMapSamplersAs2DArray.cpp
    src/compiler/translator/tree_ops/RewriteCubeMapSamplersAs2DArray.h
    src/compiler/translator/tree_ops/RewriteDfdy.cpp
    src/compiler/translator/tree_ops/RewriteDfdy.h
    src/compiler/translator/tree_ops/RewriteDoWhile.cpp
    src/compiler/translator/tree_ops/RewriteDoWhile.h
    src/compiler/translator/tree_ops/RewriteExpressionsWithShaderStorageBlock.cpp
    src/compiler/translator/tree_ops/RewriteExpressionsWithShaderStorageBlock.h
    src/compiler/translator/tree_ops/RewriteStructSamplers.cpp
    src/compiler/translator/tree_ops/RewriteStructSamplers.h
    src/compiler/translator/tree_ops/RewriteRepeatedAssignToSwizzled.cpp
    src/compiler/translator/tree_ops/RewriteRepeatedAssignToSwizzled.h
    src/compiler/translator/tree_ops/RewriteTexelFetchOffset.cpp
    src/compiler/translator/tree_ops/RewriteTexelFetchOffset.h
    src/compiler/translator/tree_ops/RewriteUnaryMinusOperatorFloat.cpp
    src/compiler/translator/tree_ops/RewriteUnaryMinusOperatorFloat.h
    src/compiler/translator/tree_ops/RewriteUnaryMinusOperatorInt.cpp
    src/compiler/translator/tree_ops/RewriteUnaryMinusOperatorInt.h
    src/compiler/translator/tree_ops/ScalarizeVecAndMatConstructorArgs.cpp
    src/compiler/translator/tree_ops/ScalarizeVecAndMatConstructorArgs.h
    src/compiler/translator/tree_ops/SeparateDeclarations.cpp
    src/compiler/translator/tree_ops/SeparateDeclarations.h
    src/compiler/translator/tree_ops/SimplifyLoopConditions.cpp
    src/compiler/translator/tree_ops/SimplifyLoopConditions.h
    src/compiler/translator/tree_ops/SplitSequenceOperator.cpp
    src/compiler/translator/tree_ops/SplitSequenceOperator.h
    src/compiler/translator/tree_ops/UnfoldShortCircuitAST.cpp
    src/compiler/translator/tree_ops/UnfoldShortCircuitAST.h
    src/compiler/translator/tree_ops/UseInterfaceBlockFields.cpp
    src/compiler/translator/tree_ops/UseInterfaceBlockFields.h
    src/compiler/translator/tree_ops/VectorizeVectorScalarArithmetic.cpp
    src/compiler/translator/tree_ops/VectorizeVectorScalarArithmetic.h
    src/compiler/translator/tree_util/BuiltIn_autogen.h
    src/compiler/translator/tree_util/FindFunction.cpp
    src/compiler/translator/tree_util/FindFunction.h
    src/compiler/translator/tree_util/FindMain.cpp
    src/compiler/translator/tree_util/FindMain.h
    src/compiler/translator/tree_util/FindSymbolNode.cpp
    src/compiler/translator/tree_util/FindSymbolNode.h
    src/compiler/translator/tree_util/IntermNodePatternMatcher.cpp
    src/compiler/translator/tree_util/IntermNodePatternMatcher.h
    src/compiler/translator/tree_util/IntermNode_util.cpp
    src/compiler/translator/tree_util/IntermNode_util.h
    src/compiler/translator/tree_util/IntermTraverse.cpp
    src/compiler/translator/tree_util/IntermTraverse.h
    src/compiler/translator/tree_util/NodeSearch.h
    src/compiler/translator/tree_util/ReplaceVariable.cpp
    src/compiler/translator/tree_util/ReplaceVariable.h
    src/compiler/translator/tree_util/ReplaceShadowingVariables.cpp
    src/compiler/translator/tree_util/ReplaceShadowingVariables.h
    src/compiler/translator/tree_util/RunAtTheEndOfShader.cpp
    src/compiler/translator/tree_util/RunAtTheEndOfShader.h
    src/compiler/translator/tree_util/Visit.h
    src/third_party/compiler/ArrayBoundsClamper.cpp
    src/third_party/compiler/ArrayBoundsClamper.h
)

set(angle_translator_essl_sources
    src/compiler/translator/OutputESSL.cpp
    src/compiler/translator/OutputESSL.h
    src/compiler/translator/TranslatorESSL.cpp
    src/compiler/translator/TranslatorESSL.h
)

set(angle_translator_glsl_sources
    src/compiler/translator/BuiltInFunctionEmulatorGLSL.cpp
    src/compiler/translator/BuiltInFunctionEmulatorGLSL.h
    src/compiler/translator/ExtensionGLSL.cpp
    src/compiler/translator/ExtensionGLSL.h
    src/compiler/translator/OutputGLSL.cpp
    src/compiler/translator/OutputGLSL.h
    src/compiler/translator/OutputGLSLBase.cpp
    src/compiler/translator/OutputGLSLBase.h
    src/compiler/translator/TranslatorGLSL.cpp
    src/compiler/translator/TranslatorGLSL.h
    src/compiler/translator/VersionGLSL.cpp
    src/compiler/translator/VersionGLSL.h
)

set(angle_translator_hlsl_sources
    src/compiler/translator/ASTMetadataHLSL.cpp
    src/compiler/translator/ASTMetadataHLSL.h
    src/compiler/translator/AtomicCounterFunctionHLSL.cpp
    src/compiler/translator/AtomicCounterFunctionHLSL.h
    src/compiler/translator/blocklayoutHLSL.cpp
    src/compiler/translator/blocklayoutHLSL.h
    src/compiler/translator/BuiltInFunctionEmulatorHLSL.cpp
    src/compiler/translator/BuiltInFunctionEmulatorHLSL.h
    src/compiler/translator/OutputHLSL.cpp
    src/compiler/translator/OutputHLSL.h
    src/compiler/translator/ResourcesHLSL.cpp
    src/compiler/translator/ResourcesHLSL.h
    src/compiler/translator/ShaderStorageBlockFunctionHLSL.cpp
    src/compiler/translator/ShaderStorageBlockFunctionHLSL.h
    src/compiler/translator/ShaderStorageBlockOutputHLSL.cpp
    src/compiler/translator/ShaderStorageBlockOutputHLSL.h
    src/compiler/translator/StructureHLSL.cpp
    src/compiler/translator/StructureHLSL.h
    src/compiler/translator/TextureFunctionHLSL.cpp
    src/compiler/translator/TextureFunctionHLSL.h
    src/compiler/translator/ImageFunctionHLSL.cpp
    src/compiler/translator/ImageFunctionHLSL.h
    src/compiler/translator/TranslatorHLSL.cpp
    src/compiler/translator/TranslatorHLSL.h
    src/compiler/translator/UtilsHLSL.cpp
    src/compiler/translator/UtilsHLSL.h
    src/compiler/translator/emulated_builtin_functions_hlsl_autogen.cpp
    src/compiler/translator/tree_ops/AddDefaultReturnStatements.cpp
    src/compiler/translator/tree_ops/AddDefaultReturnStatements.h
    src/compiler/translator/tree_ops/ArrayReturnValueToOutParameter.cpp
    src/compiler/translator/tree_ops/ArrayReturnValueToOutParameter.h
    src/compiler/translator/tree_ops/RemoveDynamicIndexing.cpp
    src/compiler/translator/tree_ops/RemoveDynamicIndexing.h
    src/compiler/translator/tree_ops/RemoveSwitchFallThrough.cpp
    src/compiler/translator/tree_ops/RemoveSwitchFallThrough.h
    src/compiler/translator/tree_ops/RewriteElseBlocks.cpp
    src/compiler/translator/tree_ops/RewriteElseBlocks.h
    src/compiler/translator/tree_ops/SeparateArrayConstructorStatements.cpp
    src/compiler/translator/tree_ops/SeparateArrayConstructorStatements.h
    src/compiler/translator/tree_ops/SeparateArrayInitialization.cpp
    src/compiler/translator/tree_ops/SeparateArrayInitialization.h
    src/compiler/translator/tree_ops/SeparateExpressionsReturningArrays.cpp
    src/compiler/translator/tree_ops/SeparateExpressionsReturningArrays.h
    src/compiler/translator/tree_ops/UnfoldShortCircuitToIf.cpp
    src/compiler/translator/tree_ops/UnfoldShortCircuitToIf.h
    src/compiler/translator/tree_ops/WrapSwitchStatementsInBlocks.cpp
    src/compiler/translator/tree_ops/WrapSwitchStatementsInBlocks.h
)

set(angle_translator_lib_vulkan_sources
    src/compiler/translator/OutputVulkanGLSL.cpp
    src/compiler/translator/OutputVulkanGLSL.h
    src/compiler/translator/TranslatorVulkan.cpp
    src/compiler/translator/TranslatorVulkan.h
)

set(angle_preprocessor_sources
    src/compiler/preprocessor/DiagnosticsBase.cpp
    src/compiler/preprocessor/DiagnosticsBase.h
    src/compiler/preprocessor/DirectiveHandlerBase.cpp
    src/compiler/preprocessor/DirectiveHandlerBase.h
    src/compiler/preprocessor/DirectiveParser.cpp
    src/compiler/preprocessor/DirectiveParser.h
    src/compiler/preprocessor/ExpressionParser.cpp
    src/compiler/preprocessor/ExpressionParser.h
    src/compiler/preprocessor/Input.cpp
    src/compiler/preprocessor/Input.h
    src/compiler/preprocessor/Lexer.cpp
    src/compiler/preprocessor/Lexer.h
    src/compiler/preprocessor/Macro.cpp
    src/compiler/preprocessor/Macro.h
    src/compiler/preprocessor/MacroExpander.cpp
    src/compiler/preprocessor/MacroExpander.h
    src/compiler/preprocessor/Preprocessor.cpp
    src/compiler/preprocessor/Preprocessor.h
    src/compiler/preprocessor/SourceLocation.h
    src/compiler/preprocessor/Token.cpp
    src/compiler/preprocessor/Token.h
    src/compiler/preprocessor/Tokenizer.cpp
    src/compiler/preprocessor/Tokenizer.h
    src/compiler/preprocessor/numeric_lex.h
)
